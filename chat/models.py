from django.db import models
from django.conf import settings
from b2b.models import B2BPost


class ChatThread(models.Model):
    post = models.ForeignKey(B2BPost, on_delete=models.CASCADE, related_name="threads")

    # seller = post.author
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads_as_seller")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads_as_buyer")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "seller", "buyer")
        indexes = [
            models.Index(fields=["seller", "created_at"]),
            models.Index(fields=["buyer", "created_at"]),
        ]

    def __str__(self):
        return f"thread:{self.id} post:{self.post_id} {self.seller_id}->{self.buyer_id}"


class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_messages")

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["thread", "created_at"]),
        ]
        ordering = ["created_at"]

    def __str__(self):
        return f"msg:{self.id} thread:{self.thread_id} sender:{self.sender_id}"
