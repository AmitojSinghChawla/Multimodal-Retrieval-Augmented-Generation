# Multimodal Retrieval-Augmented Generation (RAG) System

A production-ready multimodal RAG system that processes PDFs containing text, tables, and images, enabling intelligent question-answering through semantic search and LLM-powered retrieval.

## 🌟 Features

- **Multimodal Document Processing**: Extract and process text, tables, and images from PDFs
- **Intelligent Chunking**: Smart document segmentation using `unstructured` library
- **Semantic Search**: Vector-based retrieval using ChromaDB and HuggingFace embeddings
- **Multi-Vector Retrieval**: Separate handling of text, table, and image summaries
- **Dual Interface**: 
  - Web-based Streamlit UI
  - Command-line interface for automation
- **LLM Integration**: 
  - Ollama for local summarization (Gemma 2B, LLaVA 7B)
  - Google Gemini for response generation
- **Evaluation Pipeline**: RAGAS-based evaluation with OpenAI GPT-4

## 📋 Prerequisites

- Python 3.8+
- Ollama installed and running
- Google API key (for Gemini)
- OpenAI API key (for evaluation)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Multimodal-Retrieval-Augmented-Generation
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Ollama models**
```bash
ollama pull gemma:2b
ollama pull llava:7b
```

5. **Set up environment variables**
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 📁 Project Structure

```
App/
├── Ingestion.py              # PDF extraction and chunking
├── Ingestion_chain.py        # End-to-end ingestion pipeline
├── summarizer.py             # Text, table, and image summarization
├── VectorDB.py               # Vector database operations
├── retrieval_chain.py        # Query processing and response generation
├── app.py                    # Streamlit web interface
├── console_app.py            # Command-line interface
├── ollama_running.py         # Ollama service management
└── test_set_generator.ipynb  # RAGAS evaluation notebook
```

## 💻 Usage

### Web Interface (Streamlit)

```bash
streamlit run App/app.py
```

Features:
- Upload multiple PDFs through drag-and-drop
- Real-time processing status
- Interactive chat interface
- Session management with cleanup
- Visual feedback for all operations

### Command-Line Interface

```bash
python App/console_app.py
```

Menu options:
1. **Ingest Files**: Process PDFs and add to vector database
2. **Chat with Documents**: Interactive Q&A session
3. **Exit**: Clean up and terminate

## 🔧 Core Components

### 1. Document Ingestion

**`Ingestion.py`**
- Extracts structured elements from PDFs using `unstructured`
- Supports high-resolution image extraction
- Intelligent chunking with configurable parameters
- Separates text, tables, and images

```python
elements = create_chunks_from_pdf(file_path)
tables, texts = table_text_segregation(elements)
images = get_images(elements)
```

### 2. Summarization Pipeline

**`summarizer.py`**
- **Text/Tables**: Gemma 2B via Ollama (150-250 word summaries)
- **Images**: LLaVA 7B via Ollama (detailed visual descriptions)
- Batch processing for efficiency
- Configurable temperature and concurrency

### 3. Vector Database

**`VectorDB.py`**
- **Embedding Model**: BAAI/bge-small-en-v1.5
- **Storage**: ChromaDB with persistent storage
- **Architecture**: MultiVectorRetriever pattern
  - Summaries → vector store (for search)
  - Original content → document store (for context)
- Automatic ID generation and metadata tracking

### 4. Retrieval & Generation

**`retrieval_chain.py`**
- Google Gemini 2.0 Flash for response generation
- Context-aware prompting
- Image and text parsing
- Structured output handling

## 📊 Evaluation

The system includes a comprehensive evaluation pipeline using RAGAS:

### Metrics
- **Context Recall**: Ground truth coverage
- **Context Precision**: Relevance ranking
- **Faithfulness**: Answer-context consistency
- **Factual Correctness**: F1-based accuracy
- **Answer Relevancy**: Query alignment
- **Semantic Similarity**: Reference comparison

### Running Evaluation

```bash
jupyter notebook App/test_set_generator.ipynb
```

The notebook:
1. Generates test datasets from PDFs
2. Executes queries through the RAG pipeline
3. Evaluates responses against ground truth
4. Exports results to CSV

## ⚙️ Configuration

### Chunking Parameters
```python
chunking_strategy="by_title"
max_characters=10000
combine_text_under_n_chars=2000
new_after_n_chars=6000
```

### Retrieval Parameters
```python
k=3  # Number of documents to retrieve
embedding_model="BAAI/bge-small-en-v1.5"
```

### LLM Settings
```python
# Summarization
model="gemma:2b"
temperature=0.5

# Response generation
model="gemini-2.0-flash"

```

## 🔒 Storage & Cleanup

- **Session Management**: Automatic temporary directory creation
- **Vector DB**: Persistent ChromaDB storage in `./chroma_store`
- **Automatic Cleanup**: Registered cleanup on application exit
- **Manual Reset**: Available through UI and CLI

## 🐛 Troubleshooting

### Ollama Not Running
```bash
# Check Ollama status
ollama list

# Start Ollama service
ollama serve
```

### Memory Issues
- Reduce batch size in summarization
- Decrease `k` value in retrieval
- Use smaller embedding models

### API Rate Limits
- Implement exponential backoff
- Use local models (Ollama) where possible
- Cache responses


## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Unstructured.io**: Document parsing
- **LangChain**: RAG orchestration
- **Ollama**: Local LLM inference
- **RAGAS**: Evaluation framework
- **ChromaDB**: Vector storage

