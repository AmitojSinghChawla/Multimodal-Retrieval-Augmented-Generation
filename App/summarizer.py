from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser


def summarize_texts_tables(texts, tables):
    """
    Summarize texts and tables using Ollama model.
    """
    prompt_text = """
Summarize the following table or text concisely in 1-2 sentences.
Do not add any commentary or phrases like "Here is the summary".

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
Describe the image in detail. For context,
the image is part of a research paper explaining transformers architecture.
Be specific about graphs, such as bar plots.

Image (base64): {image_base64}
"""
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOllama(model="bakllava", temperature=0.5)
    img_summary_chain = prompt | model | StrOutputParser()

    img_summaries = [img_summary_chain.invoke({"image_base64": img}) for img in images]

    return img_summaries