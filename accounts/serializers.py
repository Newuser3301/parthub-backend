from rest_framework import serializers

class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["register", "login", "reset_password"])
    channel = serializers.ChoiceField(choices=["sms", "telegram"])

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["register", "login", "reset_password"])
    code = serializers.CharField()

class SetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["register", "reset_password"])
    password = serializers.CharField(min_length=8)

class MeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    username = serializers.CharField(allow_null=True, required=False)
    telegram_id = serializers.CharField(allow_null=True, required=False)
