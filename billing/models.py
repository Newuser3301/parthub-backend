from django.db import models
from django.conf import settings
from django.utils import timezone


class Plan(models.Model):
    code = models.CharField(max_length=32, unique=True)   # basic / pro / premium
    name = models.CharField(max_length=64)
    monthly_post_limit = models.PositiveIntegerField(default=0)  # 0 = unlimited
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} (limit={self.monthly_post_limit})"


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        EXPIRED = "expired"
        CANCELED = "canceled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["ends_at"]),
        ]

    def is_active_now(self):
        if self.status != self.Status.ACTIVE:
            return False
        if self.ends_at and self.ends_at < timezone.now():
            return False
        return True

    def __str__(self):
        return f"{self.user_id} -> {self.plan.code} ({self.status})"


class MonthlyUsage(models.Model):
    """
    Oy bo‘yicha post hisoblash (limit uchun).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="monthly_usage")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    b2b_posts = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "year", "month")

    def __str__(self):
        return f"{self.user_id} {self.year}-{self.month}: {self.b2b_posts}"
