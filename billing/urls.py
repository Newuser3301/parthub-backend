from django.urls import path
from billing.views import PlansView, MySubscriptionView

urlpatterns = [
    path("billing/plans/", PlansView.as_view()),
    path("billing/me/", MySubscriptionView.as_view()),
]
