from django.urls import path
from notifications.views import MyNotificationsView, MarkReadView, MarkAllReadView

urlpatterns = [
    path("notifications/", MyNotificationsView.as_view()),
    path("notifications/read/", MarkReadView.as_view()),
    path("notifications/read-all/", MarkAllReadView.as_view()),
]
