from django.db import models
from django.conf import settings


class NotificationType(models.TextChoices):
    MESSAGE = "message"
    SYSTEM = "system"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=32, choices=NotificationType.choices)
    title = models.CharField(max_length=200, blank=True, default="")
    body = models.TextField(blank=True, default="")

    # Optional meta
    thread_id = models.IntegerField(null=True, blank=True)
    post_id = models.IntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_read", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"notif:{self.id} user:{self.user_id} {self.type} read={self.is_read}"
