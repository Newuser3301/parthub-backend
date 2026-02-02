from django.contrib import admin
from b2b.models import B2BProfile, B2BPost

@admin.register(B2BProfile)
class B2BProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_enabled", "company_name", "city", "created_at")
    search_fields = ("user__phone", "company_name", "city")
    list_filter = ("is_enabled",)

@admin.register(B2BPost)
class B2BPostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "status", "category", "price", "currency", "created_at")
    search_fields = ("title", "description", "author__phone")
    list_filter = ("status", "category")
