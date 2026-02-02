from django.contrib import admin
from notifications.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "is_read", "thread_id", "post_id", "created_at")
    search_fields = ("user__phone", "title", "body")
    list_filter = ("type", "is_read")
