from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def root_ok(request):
    return JsonResponse({"service": "parthub-backend", "ok": True})


def healthz(_request):
    return JsonResponse({"ok": True})

urlpatterns = [
    path("", root_ok),
    path("healthz", healthz),
    path("admin/", admin.site.urls),

    path("api/", include("accounts.urls")),
    path("api/", include("billing.urls")),
    path("api/", include("b2b.urls")),
    path("api/", include("chat.urls")),
    path("api/", include("notifications.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

]
