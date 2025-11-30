# 🤖 Multimodal RAG Chatbot

A Retrieval-Augmented Generation (RAG) system that processes PDFs containing text, tables, and images using multi-vector retrieval architecture.

## 🌟 Features

- **Multimodal Processing**: Extracts and processes text, tables, and images from PDFs
- **Multi-Vector Retrieval**: Summary-based indexing with parent document retrieval
- **Dual Interface**: 
  - Streamlit web UI
  - Console CLI
- **Local & Cloud LLMs**:
  - Ollama (Gemma 2B for text/tables, LLaVA 7B for images)
  - OpenAI GPT-4o-mini for answer generation
- **RAGAS Evaluation**: Built-in testing framework
- **Session Management**: Automatic cleanup on exit

---

##  Architecture

### Retrieval Flow

```
User Query
    ↓
Search Summaries (ChromaDB vector search)
    ↓
Retrieve Original Documents (InMemoryStore)
    ↓
Parse: Texts | Tables | Images
    ↓
Build Multimodal Prompt
    ↓
Generate Answer (GPT-4o-mini)
```

### Design Decisions

- **Summaries** → Indexed in ChromaDB for semantic search
- **Original Documents** → Stored in InMemoryStore (linked by UUID)
- **Session-Scoped**: Vector DB deleted on exit for privacy and clean state

---

##  Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed
- OpenAI API key

---

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama Models

```bash
ollama pull gemma:2b
ollama pull llava:7b
```

### 3. Configure Environment

Create `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

---

##  Quick Start

### Web Interface

```bash
streamlit run app.py
```

1. Upload PDFs via sidebar
2. Click "Process Files"
3. Ask questions in chat

### Console Interface

```bash
python console_app.py
```

Commands:
- `1` - Ingest Files
- `2` - Chat with Documents
- `3` - Exit

---

##  Project Structure

```
├── Ingestion.py              # PDF extraction (unstructured library)
├── Ingestion_chain.py        # Ingestion pipeline
├── summarizer.py             # Ollama-based summarization
├── VectorDB.py               # Multi-vector retriever (ChromaDB + InMemoryStore)
├── retrieval_chain.py        # Query processing & answer generation
├── ollama_running.py         # Ollama startup utility
├── app.py                    # Streamlit web interface
├── console_app.py            # Console CLI
├── utils.py                  # Helper functions
├── test_set_generator.ipynb  # RAGAS evaluation notebook
├── requirements.txt          # Dependencies
└── .env                      # Environment variables
```

---

## ⚙️ Configuration

### Paths (console_app.py)

```python
VECTOR_DB_DIR = r"D:\Projects\Multimodal-Retrieval-Augmented-Generation\chroma_store"
DATA_DIR = r"D:\Projects\Multimodal-Retrieval-Augmented-Generation\uploaded_pdfs"
```

### Summarization (summarizer.py)

Current setting (concise):
```python
prompt_text = """
Summarize the following table or text concisely in 1-2 sentences.
Do not add any commentary or phrases like "Here is the summary".

Input: {element}
"""
```

To use detailed summaries, uncomment the alternative prompt in `summarizer.py`.

### Retrieval

Default: `k=3` documents retrieved per query

Modify in `retrieval_chain.py`:
```python
return retriever.invoke(question, kw_args={"k": 3})
```

---

## 🧪 Evaluation

### Run RAGAS Tests

```bash
jupyter notebook test_set_generator.ipynb
```

### Current Performance

Based on "Attention Is All You Need" paper (15 queries):

| Metric | Score |
|--------|-------|
| Context Recall | 0.91 |
| Context Precision | 0.90 |
| Faithfulness | 0.79 |
| Factual Correctness | 0.50 |
| Answer Relevancy | 0.82 |
| Semantic Similarity | 0.92 |

**Average: 0.82**

---

## 🔧 Troubleshooting

### Ollama Not Running

```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### ChromaDB Errors

```bash
# Delete vector database
rm -rf chroma_store/
```

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📊 Components Explained

### Ingestion.py
- Uses `unstructured` library's `partition_pdf`
- Extracts: text chunks, tables (as HTML), images (base64)
- Chunking strategy: `by_title`, max 10k chars

### summarizer.py
- Text/Tables: Ollama Gemma 2B (concise summaries)
- Images: Ollama LLaVA 7B (technical descriptions)

### VectorDB.py
- **MultiVectorRetriever** from LangChain
- Embeddings: `BAAI/bge-small-en-v1.5` (HuggingFace)
- Summaries → ChromaDB (semantic search)
- Originals → InMemoryStore (retrieval)

### retrieval_chain.py
- Builds multimodal prompt (text + images as base64)
- Uses OpenAI GPT-4o-mini for final answers
- Temperature: 0 (deterministic)

### app.py
- Streamlit web interface
- Session-scoped vector DB
- Auto-cleanup on exit or reset

### console_app.py
- CLI with PrettyTable menu
- Global retriever instance
- Cleanup with `@atexit.register`

---

## 🎯 Usage Examples

### Programmatic

```python
from VectorDB import initialize_vector_db
from Ingestion_chain import ingestion_chain
from retrieval_chain import answer_question

# Initialize
retriever = initialize_vector_db("./chroma_store")

# Ingest PDF
ingestion_chain("paper.pdf", retriever)

# Query
answer = answer_question("What is self-attention?", retriever)
print(answer)
```

### Batch Processing

```python
import os
from console_app import initialize_retriever
from Ingestion_chain import ingestion_chain

ret = initialize_retriever()

for file in os.listdir("./pdfs"):
    if file.endswith(".pdf"):
        ingestion_chain(f"./pdfs/{file}", ret)
```

---

## 🛠️ Known Limitations

1. **InMemoryStore**: Original documents not persisted between sessions (by design)
2. **Single-user**: No concurrent user support
3. **No conversation history**: Each query is independent
4. **Local summarization**: Requires Ollama running (CPU/GPU dependent)

---

## 📝 Dependencies

### Core
- `langchain`, `langchain-core`, `langchain-community`
- `langchain-openai`, `langchain-ollama`, `langchain-huggingface`
- `langchain-chroma`, `langchain-classic`

### Document Processing
- `unstructured[pdf]`
- `chromadb`
- `sentence-transformers`

### UI
- `streamlit`
- `prettytable`

### Utilities
- `python-dotenv`
- `pandas`

### Evaluation
- `ragas`
- `openai`

---

## Developer

**Amitoj Singh Chawla**

---

## 📄 License

MIT License - See LICENSE file

---

## Acknowledgments

- LangChain for RAG framework
- Unstructured for PDF processing
- RAGAS for evaluation metrics
- Ollama for local LLM inference