from django.contrib import admin
from billing.models import Plan, Subscription, MonthlyUsage

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "monthly_post_limit", "is_active", "created_at")
    search_fields = ("code", "name")
    list_filter = ("is_active",)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "status", "starts_at", "ends_at", "created_at")
    search_fields = ("user__phone", "plan__code")
    list_filter = ("status", "plan__code")

@admin.register(MonthlyUsage)
class MonthlyUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "year", "month", "b2b_posts")
    search_fields = ("user__phone",)
    list_filter = ("year", "month")
