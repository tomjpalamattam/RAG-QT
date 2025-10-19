from fastapi import FastAPI
from pydantic import BaseModel
#from rag import conversational_rag_chain
from embed import index_documents  # your embedding logic
from load_files import load_documents  # your document loader
from rag import ask_rag

app = FastAPI()


# === Data Models ===
class EmbedRequest(BaseModel):
    dir_path: str


class QueryRequest(BaseModel):
    question: str
    session_id: str = "default" 


# === Endpoints ===
@app.post("/embed")
async def embed_docs(req: EmbedRequest):
    """
    Endpoint to embed documents from a given directory.
    """
    try:
        # You can modify create_embeddings() to internally call Qdrant index
        index_documents(req.dir_path)
        return {"status": "success", "message": f"Embedded docs from {req.dir_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/query")
async def query_docs(req: QueryRequest):
    """
    Endpoint to handle RAG question-answering.
    """
    try:
        answer, context, history = ask_rag(req.question, session_id=req.session_id)
        return {
            "answer": answer,
            "context": context,
            "history": history
        }
    except Exception as e:
        return {"answer": "", "error": str(e)}
