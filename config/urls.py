from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

def healthz(_request):
    return JsonResponse({"ok": True})

urlpatterns = [
    path("healthz", healthz),
    path("admin/", admin.site.urls),

    path("api/", include("accounts.urls")),
    path("api/", include("billing.urls")),
    path("api/", include("b2b.urls")),
    path("api/", include("chat.urls")),
    path("api/", include("notifications.urls")),
]
