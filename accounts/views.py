from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

import os
DEV_OTP = os.getenv("DEV_OTP", "0") == "1"


from accounts.serializers import (
    RequestOTPSerializer, VerifyOTPSerializer, SetPasswordSerializer, MeSerializer
)
from accounts.services.otp import (
    check_rate_limit, mark_rate_limit_hit, create_otp, verify_otp
)
from accounts.services.notify import send_sms, send_telegram

User = get_user_model()


def tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class RequestOTPView(APIView):
    permission_classes = [AllowAny]



    def post(self, request):
        ser = RequestOTPSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        phone = ser.validated_data["phone"].strip()
        purpose = ser.validated_data["purpose"]
        channel = ser.validated_data["channel"]

        user = User.objects.filter(phone=phone).first()

        # Flow rules
        if purpose == "register" and user:
            return Response({"detail": "Bu raqam ro‘yxatdan o‘tgan"}, status=400)
        if purpose in ("login", "reset_password") and not user:
            return Response({"detail": "Bu raqam topilmadi"}, status=404)

        ok, msg = check_rate_limit(phone, purpose)
        if not ok:
            return Response({"detail": msg}, status=429)

        otp, code = create_otp(phone, purpose, channel, ttl_minutes=5)
        mark_rate_limit_hit(phone, purpose)

        DEV_OTP = os.getenv("DEV_OTP", "0") == "1"
        if DEV_OTP:
            return Response({"detail": "OTP yuborildi (DEV)", "code": code}, status=200)

        text = f"Kod: {code} (5 daqiqa amal qiladi)"

        if channel == "sms":
            sent = send_sms(phone, text)
        else:
            if not user or not user.telegram_id:
                return Response({"detail": "Telegram bog‘lanmagan"}, status=400)
            sent = send_telegram(user.telegram_id, text)

        if not sent:
            return Response({"detail": "OTP yuborilmadi (provider/config)"}, status=502)

        return Response({"detail": "OTP yuborildi"}, status=200)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = VerifyOTPSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        phone = ser.validated_data["phone"].strip()
        purpose = ser.validated_data["purpose"]
        code = ser.validated_data["code"].strip()

        ok, msg = verify_otp(phone, purpose, code)
        if not ok:
            return Response({"detail": msg}, status=400)

        if purpose == "login":
            user = User.objects.get(phone=phone)
            return Response({"detail": "OK", "tokens": tokens_for_user(user)}, status=200)

        # register/reset: frontend keyin set-password qiladi
        return Response({"detail": "OK"}, status=200)


class SetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = SetPasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        phone = ser.validated_data["phone"].strip()
        password = ser.validated_data["password"]

        user, _ = User.objects.get_or_create(phone=phone)
        user.set_password(password)
        user.save()

        return Response({"detail": "Parol o‘rnatildi", "tokens": tokens_for_user(user)}, status=200)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {"phone": user.phone, "username": user.username, "telegram_id": user.telegram_id}
        return Response(MeSerializer(data).data, status=200)
