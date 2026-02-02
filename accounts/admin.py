from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import PhoneOTP, OTPRequestLog

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "username", "telegram_id", "is_active", "is_staff", "created_at")
    search_fields = ("phone", "username", "telegram_id")
    list_filter = ("is_active", "is_staff")

@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "purpose", "channel", "expires_at", "attempts_left", "is_used", "created_at")
    search_fields = ("phone",)
    list_filter = ("purpose", "channel", "is_used")

@admin.register(OTPRequestLog)
class OTPRequestLogAdmin(admin.ModelAdmin):
    list_display = ("phone", "purpose", "last_requested_at", "counter_10min", "window_started_at")
    search_fields = ("phone",)
    list_filter = ("purpose",)
