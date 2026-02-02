from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from billing.models import Plan
from billing.services import get_active_subscription, get_effective_plan
from billing.serializers import PlanSerializer, SubscriptionSerializer


class PlansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.filter(is_active=True).order_by("id")
        data = [{"code": p.code, "name": p.name, "monthly_post_limit": p.monthly_post_limit} for p in plans]
        return Response(data, status=200)


class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sub = get_active_subscription(request.user)
        if sub:
            data = {
                "plan_code": sub.plan.code,
                "status": sub.status,
                "starts_at": sub.starts_at,
                "ends_at": sub.ends_at,
            }
            return Response(data, status=200)

        # fallback basic
        plan = get_effective_plan(request.user)
        return Response({
            "plan_code": plan.code,
            "status": "fallback",
            "starts_at": None,
            "ends_at": None,
        }, status=200)
