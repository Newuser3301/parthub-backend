from rest_framework import serializers
from chat.models import ChatThread, ChatMessage

class ThreadSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)
    seller_phone = serializers.CharField(source="seller.phone", read_only=True)
    buyer_phone = serializers.CharField(source="buyer.phone", read_only=True)

    class Meta:
        model = ChatThread
        fields = ("id", "post_id", "post_title", "seller_phone", "buyer_phone", "created_at")


class MessageSerializer(serializers.ModelSerializer):
    sender_phone = serializers.CharField(source="sender.phone", read_only=True)

    class Meta:
        model = ChatMessage
        fields = ("id", "thread", "sender_phone", "text", "created_at")
        read_only_fields = ("id", "sender_phone", "created_at")
