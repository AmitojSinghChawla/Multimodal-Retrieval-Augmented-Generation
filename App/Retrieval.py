from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from base64 import b64decode
from dotenv import load_dotenv
import os


load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

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
        except Exception:
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

# --- Build the LangChain chain ---
chain = (
    {
        "context": retriever_func | RunnableLambda(parse_docs),  # pass function, not called
        "question": RunnablePassthrough(),
    }
    | RunnableLambda(build_prompt)
    | StrOutputParser()
)

# --- Main function ---
def answer_question(question):
    # Optional: handle greetings quickly
    if question.lower().strip() in ["hi", "hello", "hey"]:
        return "Hello! How can I help you today?"

    # Retrieve and filter docs with actual content
    retrieved_docs = [
        doc for doc in retriever_func(question)
        if getattr(doc, "page_content", "").strip()
    ]

    # Zero-shot fallback if no real content
    if not retrieved_docs:
        prompt = f"Answer the question based on your knowledge. No relevant content found. Question: {question}"
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    # Normal RAG path
    context = parse_docs(retrieved_docs)
    prompt_parts = build_prompt(context, question)
    response = llm.invoke(prompt_parts)
    return response.content
