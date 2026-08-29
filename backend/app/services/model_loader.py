"""
Shared embedding model singleton for all Synaptrix agents.
Loads one model (all-MiniLM-L6-v2, ~90MB) instead of multiple models.
"""
from sentence_transformers import SentenceTransformer
import os
import time

_model = None


def get_embedding_model():
    """Get the shared embedding model instance (lazy-loaded singleton)."""
    global _model

    if _model is None:
        print("🔥 Loading shared embedding model...")
        start = time.time()

        cache_dir = os.environ.get("HF_HOME", os.environ.get("MODEL_CACHE_DIR", "./models"))

        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=cache_dir
        )

        print(f"✅ Embedding model loaded in {round(time.time() - start, 2)}s")

    return _model


def warmup_model():
    """Pre-load the model during startup."""
    get_embedding_model()
    print("✅ Embedding model warm and ready")
