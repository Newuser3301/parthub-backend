from django.urls import path
from chat.views import MyThreadsView, StartThreadView, ThreadMessagesView, SendMessageView

urlpatterns = [
    path("chat/threads/", MyThreadsView.as_view()),
    path("chat/start/", StartThreadView.as_view()),
    path("chat/threads/<int:thread_id>/messages/", ThreadMessagesView.as_view()),
    path("chat/send/", SendMessageView.as_view()),
]
