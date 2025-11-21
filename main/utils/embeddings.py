import os
import pickle
import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer
from django.conf import settings

# -------------------------------
# Config
# -------------------------------
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CACHE_DIR = os.path.join(settings.BASE_DIR, "vector_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Load embedding model once globally
embedder = SentenceTransformer(EMBED_MODEL_NAME)


def get_embedding_model():
    """
    Returns the globally loaded SentenceTransformer embedder.
    Use this instead of creating new instances in other modules.
    """
    return embedder


# -------------------------------
# Text Chunking
# -------------------------------
def chunk_text(text, max_words=200):
    """
    Split text into smaller semantic chunks based on sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, chunk, count = [], [], 0

    for sentence in sentences:
        words = sentence.split()
        count += len(words)
        chunk.append(sentence)

        if count >= max_words:
            chunks.append(" ".join(chunk))
            chunk, count = [], 0

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks


# -------------------------------
# Embedding Manager
# -------------------------------
class EmbeddingManager:
    """
    Handles FAISS-based document embeddings with caching.
    """

    def __init__(self, storage_key: str):
        self.storage_key = storage_key
        self.cache_path = os.path.join(CACHE_DIR, f"{storage_key}_index.pkl")
        self.index = None
        self.chunks = None

    def _save_cache(self, embeddings, chunks):
        """Save FAISS index and chunks to disk."""
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings.astype(np.float32))

        with open(self.cache_path, "wb") as f:
            pickle.dump({"index": index, "chunks": chunks}, f)

    def _load_cache(self):
        """Load FAISS index and chunks if cache exists."""
        if not os.path.exists(self.cache_path):
            return None
        with open(self.cache_path, "rb") as f:
            data = pickle.load(f)
            return data["index"], data["chunks"]

    def build_index(self, text):
        """Create and cache FAISS index for a document."""
        chunks = chunk_text(text)
        embeddings = embed_texts(chunks)
        self._save_cache(embeddings, chunks)
        self.index, self.chunks = self._load_cache()
        return True

    def load_or_build(self, text):
        """Load cached FAISS or build new one."""
        data = self._load_cache()
        if data:
            self.index, self.chunks = data
            return
        self.build_index(text)

    def retrieve(self, query, top_k=3):
        """Retrieve most similar chunks for a query."""
        if not self.index or not self.chunks:
            raise ValueError("Index not loaded. Call load_or_build() first.")

        q_emb = embed_texts([query]).astype(np.float32)
        distances, indices = self.index.search(q_emb, top_k)
        return [self.chunks[i] for i in indices[0]]


# -------------------------------
# Helper for embedding anywhere
# -------------------------------
def embed_texts(texts):
    """
    Generate embeddings for a list (or single) text using the shared model.
    """
    if isinstance(texts, str):
        texts = [texts]
    return embedder.encode(texts)