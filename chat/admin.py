from django.contrib import admin
from chat.models import ChatThread, ChatMessage

@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "seller", "buyer", "created_at")
    search_fields = ("seller__phone", "buyer__phone", "post__title")

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "sender", "created_at")
    search_fields = ("sender__phone", "thread__id")
