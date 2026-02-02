import os
import requests

# ---------- Telegram ----------
def send_telegram(telegram_id: str, text: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        return False

    telegram_id = str(telegram_id).strip()
    if not telegram_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": text,
        "disable_web_page_preview": True,
    }

    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code != 200:
            return False
        data = r.json()
        return bool(data.get("ok") is True)
    except Exception:
        return False


# ---------- Eskiz SMS ----------
_ESKIZ_TOKEN = None

def _eskiz_login() -> str | None:
    global _ESKIZ_TOKEN

    email = os.getenv("ESKIZ_EMAIL")
    password = os.getenv("ESKIZ_PASSWORD")
    base = os.getenv("ESKIZ_BASE_URL", "https://notify.eskiz.uz/api").rstrip("/")

    if not email or not password:
        return None

    try:
        r = requests.post(f"{base}/auth/login", json={"email": email, "password": password}, timeout=20)
        if r.status_code != 200:
            return None
        data = r.json()
        token = (data.get("data") or {}).get("token")
        if token:
            _ESKIZ_TOKEN = token
        return _ESKIZ_TOKEN
    except Exception:
        return None


def send_sms(phone: str, text: str) -> bool:
    global _ESKIZ_TOKEN

    sender = os.getenv("ESKIZ_FROM")
    base = os.getenv("ESKIZ_BASE_URL", "https://notify.eskiz.uz/api").rstrip("/")

    if not sender:
        return False

    phone = phone.strip()
    if not phone:
        return False

    if not _ESKIZ_TOKEN:
        if not _eskiz_login():
            return False

    url = f"{base}/message/sms/send"
    headers = {"Authorization": f"Bearer {_ESKIZ_TOKEN}"}
    payload = {"mobile_phone": phone, "message": text, "from": sender}

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        if r.status_code == 200:
            return True

        # token o‘lib qolsa 1 marta refresh qilib ko‘ramiz
        if r.status_code in (401, 403):
            _ESKIZ_TOKEN = None
            if not _eskiz_login():
                return False
            headers = {"Authorization": f"Bearer {_ESKIZ_TOKEN}"}
            r2 = requests.post(url, json=payload, headers=headers, timeout=20)
            return r2.status_code == 200

        return False
    except Exception:
        return False
