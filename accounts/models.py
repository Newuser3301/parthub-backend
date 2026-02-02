from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone is required")
        phone = phone.strip()
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    telegram_id = models.CharField(max_length=64, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone


class OTPPurpose(models.TextChoices):
    REGISTER = "register"
    LOGIN = "login"
    RESET_PASSWORD = "reset_password"


class OTPChannel(models.TextChoices):
    SMS = "sms"
    TELEGRAM = "telegram"


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    code_hash = models.CharField(max_length=128)

    purpose = models.CharField(max_length=32, choices=OTPPurpose.choices)
    channel = models.CharField(max_length=16, choices=OTPChannel.choices)

    expires_at = models.DateTimeField()
    attempts_left = models.IntegerField(default=5)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def default_expiry(minutes=5):
        return timezone.now() + timedelta(minutes=minutes)

    def __str__(self):
        return f"{self.phone} {self.purpose} {self.channel}"


class OTPRequestLog(models.Model):
    """
    Rate-limit uchun: har phone/purpose bo‘yicha oxirgi OTP request qachon bo‘lganini saqlaymiz.
    """
    phone = models.CharField(max_length=20, db_index=True)
    purpose = models.CharField(max_length=32, choices=OTPPurpose.choices)
    last_requested_at = models.DateTimeField(default=timezone.now)
    counter_10min = models.IntegerField(default=0)  # optional: spam control
    window_started_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("phone", "purpose")

    def __str__(self):
        return f"{self.phone} {self.purpose}"
