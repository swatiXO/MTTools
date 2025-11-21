# docs_ai/models.py
from django.db import models
import uuid

class Document(models.Model):
    title = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="uploads/")
    storage_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    num_chunks = models.IntegerField(default=0)
    extracted_text = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title


class ChatSession(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ChatSession for {self.document.title} ({self.chat_id})"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.role}] {self.text[:40]}"
