import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta

from accounts.models import PhoneOTP, OTPRequestLog


def _normalize_phone(phone: str) -> str:
    return phone.strip()


def generate_code(length=6) -> str:
    start = 10 ** (length - 1)
    end = (10 ** length) - 1
    return str(random.randint(start, end))


def check_rate_limit(phone: str, purpose: str, cooldown_seconds: int = 60, max_per_10min: int = 8):
    """
    1) Cooldown: 1 phone/purpose -> 60s ichida qayta so‘ray olmaydi
    2) 10 minutlik limit: spamdan himoya
    """
    phone = _normalize_phone(phone)
    now = timezone.now()

    log, created = OTPRequestLog.objects.get_or_create(
        phone=phone, purpose=purpose,
        defaults={"last_requested_at": now, "counter_10min": 0, "window_started_at": now}
    )

    # 10 min window
    if log.window_started_at + timedelta(minutes=10) < now:
        log.window_started_at = now
        log.counter_10min = 0

    # cooldown
    if (now - log.last_requested_at).total_seconds() < cooldown_seconds:
        wait = cooldown_seconds - int((now - log.last_requested_at).total_seconds())
        return False, f"Juda tez. {wait}s kut"

    # max per window
    if log.counter_10min >= max_per_10min:
        return False, "Juda ko‘p urinish. 10 minutdan keyin qayta urin"

    return True, "OK"


def mark_rate_limit_hit(phone: str, purpose: str):
    phone = _normalize_phone(phone)
    now = timezone.now()
    log, _ = OTPRequestLog.objects.get_or_create(phone=phone, purpose=purpose)
    log.last_requested_at = now
    log.counter_10min += 1
    log.save(update_fields=["last_requested_at", "counter_10min", "window_started_at"])


def create_otp(phone: str, purpose: str, channel: str, ttl_minutes: int = 5):
    phone = _normalize_phone(phone)
    code = generate_code(6)

    otp = PhoneOTP.objects.create(
        phone=phone,
        purpose=purpose,
        channel=channel,
        code_hash=make_password(code),
        expires_at=PhoneOTP.default_expiry(ttl_minutes),
        attempts_left=5,
        is_used=False,
    )
    return otp, code


def verify_otp(phone: str, purpose: str, code: str):
    phone = _normalize_phone(phone)
    code = code.strip()

    otp = (
        PhoneOTP.objects
        .filter(phone=phone, purpose=purpose, is_used=False)
        .order_by("-created_at")
        .first()
    )

    if not otp:
        return False, "OTP topilmadi"

    if otp.expires_at < timezone.now():
        return False, "OTP eskirgan"

    if otp.attempts_left <= 0:
        return False, "Urinishlar tugagan"

    if not check_password(code, otp.code_hash):
        otp.attempts_left -= 1
        otp.save(update_fields=["attempts_left"])
        return False, "Kod xato"

    otp.is_used = True
    otp.save(update_fields=["is_used"])
    return True, "OK"
