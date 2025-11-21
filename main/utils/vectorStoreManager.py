import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from django.conf import settings
from datetime import datetime

# -------------------------------
# Config
# -------------------------------
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CACHE_DIR = os.path.join(settings.BASE_DIR, "chat_vector_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Load embedding model globally
embedder = SentenceTransformer(EMBED_MODEL_NAME)


def get_embedding_model():
    """Return the globally loaded SentenceTransformer embedder."""
    return embedder


# -------------------------------
# Helper
# -------------------------------
def embed_texts(texts):
    """Generate embeddings for one or many texts."""
    if isinstance(texts, str):
        texts = [texts]
    return embedder.encode(texts)


# -------------------------------
# Chat Vector Store Manager
# -------------------------------
class ChatVectorManager:
    """
    Handles FAISS-based embeddings for chat history.
    Each chat message (user or assistant) is stored as a vector with metadata.
    """

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        self.cache_path = os.path.join(CACHE_DIR, f"{chat_id}_chat_index.pkl")
        self.index = None
        self.messages = None  # [(role, text, timestamp), ...]
        self._load_cache()

    # ---------------------------
    # Cache Handling
    # ---------------------------
    def _save_cache(self, embeddings, messages):
        """Save FAISS index and messages metadata."""
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings.astype(np.float32))
        with open(self.cache_path, "wb") as f:
            pickle.dump({"index": index, "messages": messages}, f)

    def _load_cache(self):
        """Load FAISS index and messages metadata from disk."""
        if not os.path.exists(self.cache_path):
            self.index = None
            self.messages = []
            return
        with open(self.cache_path, "rb") as f:
            data = pickle.load(f)
            self.index, self.messages = data["index"], data["messages"]

    # ---------------------------
    # Message Storage
    # ---------------------------
    def add_message(self, role: str, text: str):
        """
        Add a single chat message to the FAISS index.
        role: 'user' or 'assistant'
        """
        emb = embed_texts([text]).astype(np.float32)
        timestamp = datetime.utcnow().isoformat()

        # Create or extend index
        if self.index is None:
            self.index = faiss.IndexFlatL2(emb.shape[1])
            self.messages = []

        self.index.add(emb)
        self.messages.append({"role": role, "text": text, "timestamp": timestamp})
        self._save_cache(self.get_all_embeddings(), self.messages)

    def get_all_embeddings(self):
        """Rebuild embeddings from stored messages if needed."""
        texts = [m["text"] for m in self.messages]
        return embed_texts(texts)

    # ---------------------------
    # Retrieval
    # ---------------------------
    def search(self, query, top_k=5):
        """Find the most semantically similar chat messages to a query."""
        if self.index is None or not self.messages:
            return []

        q_emb = embed_texts([query]).astype(np.float32)
        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for i, dist in zip(indices[0], distances[0]):
            msg = self.messages[i]
            results.append({
                "role": msg["role"],
                "text": msg["text"],
                "timestamp": msg["timestamp"],
                "similarity": float(dist)
            })
        return results

    # ---------------------------
    # Utility
    # ---------------------------
    def clear(self):
        """Delete cache for this chat session."""
        if os.path.exists(self.cache_path):
            os.remove(self.cache_path)
        self.index = None
        self.messages = []

