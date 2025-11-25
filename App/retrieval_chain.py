import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from base64 import b64decode

load_dotenv()

# Initialize Gemini model
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
<<<<<<< HEAD
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=GEMINI_API_KEY)

=======
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GEMINI_API_KEY)
>>>>>>> 196e6167f54456da83b27d8dcf9ad4415b4e71d9


def parse_docs(docs):
    """
    Split retrieved documents into images and texts.
    """
    images = []
    texts = []
    for doc in docs:
        content = getattr(doc, "page_content", doc)

        if hasattr(content, "text"):
            text_str = content.text
        else:
            text_str = str(content)

        try:
            b64decode(text_str)
            images.append(text_str)
        except Exception as e:
            texts.append(text_str)

    return {"images": images, "texts": texts}


def build_prompt(context, question):
    """
    Build prompt for Gemini model.
    """
    text_context = "\n".join(context["texts"])
    prompt = f"""
Answer the question based only on the given context.
Context: {text_context}
Question: {question}
"""
    return [HumanMessage(content=prompt)]


def answer_question(question, retriever):
    """
    Answer a question using the retriever and Gemini model.
    """
    from VectorDB import retrieve_documents

    docs = retrieve_documents(retriever, question, k=3)
    context = parse_docs(docs)
    prompt_parts = build_prompt(context, question)
    response = llm.invoke(prompt_parts)

    return response.content