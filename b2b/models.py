from django.db import models
from django.conf import settings


class B2BProfile(models.Model):
    """
    Admin panelda: user B2B ga qo‘shiladimi yo‘qmi.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="b2b_profile")
    is_enabled = models.BooleanField(default=False)

    company_name = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=128, blank=True, default="")
    about = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} enabled={self.is_enabled}"


class PostStatus(models.TextChoices):
    ACTIVE = "active"
    CLOSED = "closed"
    HIDDEN = "hidden"


class B2BPost(models.Model):
    """
    B2B Lounge post: 'menda optom bor', 'menga kerak', etc.
    Bu mahsulot katalogi emas — post/feed.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="b2b_posts")

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(max_length=64, blank=True, default="")
    status = models.CharField(max_length=16, choices=PostStatus.choices, default=PostStatus.ACTIVE)

    # Optional "deal" fields
    qty = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=32, blank=True, default="")
    price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, blank=True, default="UZS")

    contact_phone = models.CharField(max_length=20, blank=True, default="")
    contact_telegram = models.CharField(max_length=64, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["category"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} {self.title}"
