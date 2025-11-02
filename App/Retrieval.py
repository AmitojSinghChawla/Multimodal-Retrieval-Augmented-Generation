from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from base64 import b64decode
from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API_KEY=os.getenv("GOOGLE_API_KEY")


llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=GEMINI_API_KEY)


# --- Retriever wrapper function ---
def retriever_func(question):
    from App.VectorDB import multi_retriever
    # Call the MultiVectorRetriever object, not the function itself
    docs = multi_retriever.invoke(question, kw_args={"k": 3})
    return docs  # return Document objects, not str()

# --- Split text and images ---
def parse_docs(docs):
    images = []
    texts = []
    for doc in docs:
        content = getattr(doc, "page_content", doc)

        # Convert CompositeElement to text
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

# --- Build prompt parts for Gemini ---
def build_prompt(context, question):
    text_context = "\n".join(context["texts"])
    prompt = f"""
Answer the question based only on the given context.
Context: {text_context}
Question: {question}
"""
    return [HumanMessage(content=prompt)]


# --- Complete retrieval chain ---
def retrieval_chain(question):
    try:
        # Step 1: Retrieve relevant documents
        docs = retriever_func(question)

        # Step 2: Parse documents into texts and images
        context = parse_docs(docs)

        # Step 3: Build prompt for Gemini
        messages = build_prompt(context, question)

        # Step 4: Get answer from Gemini
        response = llm.generate_messages([messages], max_tokens=500)
        answer = response.generations[0][0].message.content

        return answer

    except Exception as e:
        raise RuntimeError(f"Retrieval chain failed: {str(e)}")