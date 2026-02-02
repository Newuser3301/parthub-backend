from rest_framework import serializers
from b2b.models import B2BPost, B2BProfile

class B2BProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BProfile
        fields = ("is_enabled", "company_name", "city", "about")


class B2BPostSerializer(serializers.ModelSerializer):
    author_phone = serializers.CharField(source="author.phone", read_only=True)

    class Meta:
        model = B2BPost
        fields = (
            "id",
            "author_phone",
            "title",
            "description",
            "category",
            "status",
            "qty",
            "unit",
            "price",
            "currency",
            "contact_phone",
            "contact_telegram",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author_phone", "created_at", "updated_at")
