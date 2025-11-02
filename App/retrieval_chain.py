from App.Retrieval import parse_docs, build_prompt,retriever_func
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
from Retrieval import llm


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
