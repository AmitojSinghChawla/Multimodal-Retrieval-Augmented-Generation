from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import os

def summarize_texts_tables(texts, tables):
    """
    Summarize texts and tables using Ollama model.
    """
    prompt_text = """
Create a detailed summary (150–250 words) of the following text or table.
Include key ideas, technical details, numerical trends, structure, and context.
Avoid being vague. Write a comprehensive summary,No introductions, no filler, no meta-statements, no AI explanations, no greetings.

Input: {element}
"""
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOllama(temperature=0.5, model="gemma:2b", verbose=False)
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Summarize texts
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})

    # Summarize tables
    tables_html = [table.metadata.text_as_html for table in tables]
    table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})

    return table_summaries, text_summaries


def summarize_images(images):
    """
    Summarize images using BakLLaVA model.
    """
    prompt_text = """
Describe this image in depth (150–250 words).
Include visual structure, graphs, axes, labels, patterns, shapes,
and observations. Be precise and technical No introductions, no filler, no meta-statements, no AI explanations, no greetings.

Image (base64): {image_base64}
"""
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOllama(model="llava:7b", temperature=0.5)
    img_summary_chain = prompt | model | StrOutputParser()

    img_summaries = [img_summary_chain.invoke({"image_base64": img}) for img in images]

    return img_summaries


#