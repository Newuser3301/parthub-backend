from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from django.db import models

from chat.models import ChatThread, ChatMessage
from chat.serializers import ThreadSerializer, MessageSerializer
from b2b.models import B2BPost

from notifications.models import Notification, NotificationType


def _create_message_notification(receiver, thread, text):
    Notification.objects.create(
        user=receiver,
        type=NotificationType.MESSAGE,
        title="Yangi xabar",
        body=text[:200],
        thread_id=thread.id,
        post_id=thread.post_id,
    )


class MyThreadsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer

    def get_queryset(self):
        u = self.request.user
        return (
            ChatThread.objects
            .select_related("post", "seller", "buyer")
            .filter(models.Q(seller=u) | models.Q(buyer=u))
            .order_by("-created_at")
        )


class StartThreadView(APIView):
    """
    Buyer postdan chat ochadi:
    POST /api/chat/start/ { "post_id": 123 }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get("post_id")
        if not post_id:
            return Response({"detail": "post_id kerak"}, status=400)

        post = B2BPost.objects.select_related("author").filter(id=post_id).first()
        if not post:
            raise NotFound("Post topilmadi")

        seller = post.author
        buyer = request.user

        if seller.id == buyer.id:
            raise PermissionDenied("O‘zing bilan chat qilolmaysan 😄")

        thread, _ = ChatThread.objects.get_or_create(
            post=post,
            seller=seller,
            buyer=buyer,
        )

        return Response(ThreadSerializer(thread).data, status=200)


class ThreadMessagesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        thread_id = self.kwargs["thread_id"]
        thread = ChatThread.objects.filter(id=thread_id).first()
        if not thread:
            raise NotFound("Thread topilmadi")

        uid = self.request.user.id
        if thread.seller_id != uid and thread.buyer_id != uid:
            raise PermissionDenied("Ruxsat yo‘q")

        return ChatMessage.objects.select_related("sender").filter(thread=thread).order_by("created_at")


class SendMessageView(APIView):
    """
    POST /api/chat/send/ { "thread_id": 1, "text": "salom" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        thread_id = request.data.get("thread_id")
        text = (request.data.get("text") or "").strip()

        if not thread_id or not text:
            return Response({"detail": "thread_id va text kerak"}, status=400)

        thread = ChatThread.objects.select_related("seller", "buyer", "post").filter(id=thread_id).first()
        if not thread:
            raise NotFound("Thread topilmadi")

        uid = request.user.id
        if thread.seller_id != uid and thread.buyer_id != uid:
            raise PermissionDenied("Ruxsat yo‘q")

        msg = ChatMessage.objects.create(thread=thread, sender=request.user, text=text)

        # notify other side
        receiver = thread.buyer if thread.seller_id == uid else thread.seller
        _create_message_notification(receiver, thread, text)

        return Response(MessageSerializer(msg).data, status=201)
