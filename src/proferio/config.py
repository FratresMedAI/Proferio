from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    backend: str = Field(default="ollama", description="ollama | llamacpp | hf")
    model_name: str = Field(default="llama3.1:8b")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    vector_db: str = Field(default="faiss", description="faiss | chroma")
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5
    rerank_top_n: int = 10
    max_agent_steps: int = 6
    use_hybrid_retrieval: bool = True
    vector_weight: float = 0.65
    bm25_weight: float = 0.35
    oos_min_overlap: int = 2
    oos_score_threshold: float = 0.22
    index_path: str = "artifacts/index"
    persist_index: bool = True
