from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser


def summarize_texts_tables(texts, tables):
    """
    Summarize texts and tables using Ollama model.
    """
    # Concise summary prompt (1-2 sentences)
    prompt_text = """
Summarize the following table or text concisely in 1-2 sentences.
Do not add any commentary or phrases like "Here is the summary".

Input: {element}
"""

    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOllama(temperature=0.5, model="gemma:2b", verbose=False)
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Summarize texts
    raw_text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})
    text_summaries = [
        s if isinstance(s, str) else s.content for s in raw_text_summaries
    ]

    # Summarize tables
    tables_html = [table.metadata.text_as_html for table in tables]
    raw_table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})
    table_summaries = [
        s if isinstance(s, str) else s.content for s in raw_table_summaries
    ]

    return text_summaries, table_summaries


def summarize_images(images_b64):
    """
    Summarize images using LLaVA model.
    """
    llm = ChatOllama(model="llava", temperature=0.0)
    parser = StrOutputParser()
    summaries = []

    for b64 in images_b64:
        # Build data URL for LangChain ChatOllama wrapper
        data_url = f"data:image/jpeg;base64,{b64}"

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image accurately, in technical detail.",
                    },
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ]

        resp = llm.invoke(messages)
        summaries.append(parser.parse(resp))

    return summaries
