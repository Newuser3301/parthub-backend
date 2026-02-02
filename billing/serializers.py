from rest_framework import serializers

class PlanSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    monthly_post_limit = serializers.IntegerField()

class SubscriptionSerializer(serializers.Serializer):
    plan_code = serializers.CharField()
    status = serializers.CharField()
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField(allow_null=True)
