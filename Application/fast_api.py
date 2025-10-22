from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

from Ingestion import ingest_pdfs_to_vector_db
from utils import answer_question
from pydantic_models import QueryRequest, QueryResponse

app = FastAPI()

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    """
    Endpoint to ingest PDF files into the vector database.
    Accepts multiple PDF files uploaded via a POST request.
    """
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")

    for file in files:
        try:
            # Read file contents as bytes
            file_bytes = await file.read()
            pdf_stream = BytesIO(file_bytes)

            # Pass BytesIO directly to ingestion
            ingest_pdfs_to_vector_db(pdf_stream)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to ingest {file.filename}: {str(e)}")

    return {"success": True, "message": "All PDFs ingested successfully"}

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    question = request.query
    answer = answer_question(question)

    if not isinstance(answer, str):
        raise HTTPException(status_code=400, detail="Model response is not a string")

    return QueryResponse(answer=answer)
