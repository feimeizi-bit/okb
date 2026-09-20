import os
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
from fastapi import FastAPI
from pydantic import BaseModel
from fastembed import TextEmbedding

MODEL_NAME = os.environ.get("EMBED_MODEL", "BAAI/bge-small-zh-v1.5")
model = TextEmbedding(model_name=MODEL_NAME)

app = FastAPI()

class EmbeddingRequest(BaseModel):
    input: str | list[str]
    model: str | None = None

@app.post("/v1/embeddings")
def embeddings(req: EmbeddingRequest):
    texts = [req.input] if isinstance(req.input, str) else req.input
    vectors = [v.tolist() for v in model.embed(texts)]
    return {
        "object": "list",
        "data": [{"object": "embedding", "index": i, "embedding": v} for i, v in enumerate(vectors)],
        "model": req.model or MODEL_NAME,
        "usage": {"prompt_tokens": 0, "total_tokens": 0},
    }

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}
