from django.utils import timezone
from billing.models import Subscription, Plan, MonthlyUsage


DEFAULT_PLAN_CODE = "basic"


def get_active_subscription(user):
    sub = (
        Subscription.objects
        .select_related("plan")
        .filter(user=user, status=Subscription.Status.ACTIVE)
        .order_by("-created_at")
        .first()
    )
    if sub and sub.is_active_now():
        return sub
    return None


def get_effective_plan(user) -> Plan:
    sub = get_active_subscription(user)
    if sub:
        return sub.plan

    # fallback: basic plan (DB’da bo‘lishi kerak)
    plan = Plan.objects.filter(code=DEFAULT_PLAN_CODE, is_active=True).first()
    if not plan:
        # If DB’da yo‘q bo‘lsa, hard fail (admin yaratishi kerak)
        raise RuntimeError("Default plan (basic) is missing in DB")
    return plan


def _usage_row(user):
    now = timezone.now()
    row, _ = MonthlyUsage.objects.get_or_create(user=user, year=now.year, month=now.month)
    return row


def can_create_b2b_post(user) -> tuple[bool, str]:
    plan = get_effective_plan(user)
    limit = plan.monthly_post_limit  # 0 = unlimited

    if limit == 0:
        return True, "OK"

    usage = _usage_row(user)
    if usage.b2b_posts >= limit:
        return False, f"Limit tugadi: {usage.b2b_posts}/{limit}"
    return True, "OK"


def inc_b2b_post(user):
    usage = _usage_row(user)
    usage.b2b_posts += 1
    usage.save(update_fields=["b2b_posts"])
