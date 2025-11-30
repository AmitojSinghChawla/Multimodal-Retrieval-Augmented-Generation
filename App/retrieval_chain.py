from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from base64 import b64decode
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0
)

def retriever_func(question, retriever):
    """Use the retriever instance returned from VectorDB.initialize_vector_db"""
    return retriever.invoke(question, kw_args={"k": 3})


def parse_docs(docs):
    b64 = []
    text = []

    for doc in docs:
        content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
        try:
            b64decode(content)
            b64.append(content)
        except Exception:
            text.append(doc)

    return {"images": b64, "texts": text}


def build_prompt(kwargs):
    docs_by_type = kwargs["context"]
    user_question = kwargs["question"]

    context_text = ""
    for text_element in docs_by_type["texts"]:
        if hasattr(text_element, 'page_content'):
            context_text += text_element.page_content + "\n\n"
        else:
            context_text += str(text_element) + "\n\n"

    prompt_template = f"""Answer the question based only on the following context, which can include text, tables, and images.

Context: {context_text}

Question: {user_question}
"""

    prompt_content = [{"type": "text", "text": prompt_template}]

    for image in docs_by_type["images"]:
        prompt_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
        })

    return [HumanMessage(content=prompt_content)]


def answer_question(question, retriever):
    """MAIN FUNCTION – Uses the retriever created in VectorDB.initialize_vector_db"""
    chain_with_sources = {
        "context": (lambda q: retriever_func(q, retriever)) | RunnableLambda(parse_docs),
        "question": RunnablePassthrough(),
    } | RunnablePassthrough().assign(
        response=(
            RunnableLambda(build_prompt)
            | llm
            | StrOutputParser()
        )
    )

    response = chain_with_sources.invoke(question)
    return response['response']