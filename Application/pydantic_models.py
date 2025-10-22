from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the capital of France?")


class QueryResponse(BaseModel):
    answer: str = Field(..., example="The capital of France is Paris.")

