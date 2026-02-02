from django.urls import path
from accounts.views import RequestOTPView, VerifyOTPView, SetPasswordView, MeView

urlpatterns = [
    path("auth/request-otp/", RequestOTPView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/set-password/", SetPasswordView.as_view()),
    path("auth/me/", MeView.as_view()),
]
