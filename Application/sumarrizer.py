from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser



def summarize_texts_tables(texts, tables):
    prompt_text = """
    Summarize the following table or text concisely in 1-2 sentences.
    Do not add any commentary or phrases like "Here is the summary".

    Input: {element}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Summary chain
    model = ChatOllama(temperature=0.5, model="bakllava", verbose=False)
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Summarize text
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})

    # Summarize tables
    tables_html = [table.metadata.text_as_html for table in tables]
    table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})

    return text_summaries, table_summaries

def summarize_images(images64):
    # Prompt template
    prompt_text = """
    Describe the image in detail. For context,
    the image is part of a research paper explaining transformers architecture.
    Be specific about graphs, such as bar plots.

    Image (base64): {image_base64}
    """

    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Load the local BakLLaVA model
    model = ChatOllama(model="bakllava", temperature=0.5)

    img_summary_chain = prompt | model | StrOutputParser()

    image_summaries = img_summary_chain.invoke(images64)
