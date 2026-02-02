# Parthub Backend API 🚀
**Django 5 + Django REST Framework**

Parthub — bu **B2B marketplace backend** bo‘lib, telefon orqali login, tariflar, B2B postlar, chat va notification’larni ta’minlaydi.  
Frontend (React / Vue / Next / Mobile) ushbu backend API’ga ulanadi.

---

## 📌 Loyihaning vazifasi
- Telefon raqam orqali **OTP login / register**
- **JWT authentication** (access / refresh)
- **Tariflar (Billing)** va post limitlar
- **B2B Lounge** (post/feed)
- **Chat** (buyer ↔ seller)
- **Notification** (xabar kelganda)

---

## 📂 Folder struktura

```
backend/
├── manage.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── build.sh
├── .env
├── .gitignore
│
├── config/                         # Django project config
│   ├── __init__.py
│   ├── settings.py                 # Global settings
│   ├── urls.py                     # Root URLs
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                       # Auth + User + OTP
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # User, PhoneOTP, OTPRequestLog
│   ├── serializers.py              # OTP, password, me serializers
│   ├── views.py                    # request_otp, verify_otp, set_password, me
│   ├── urls.py                     # /api/auth/*
│   ├── permissions.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── otp.py                  # OTP generate/verify logic
│   │   ├── notify.py               # SMS / Telegram / DEV notifier
│   │   └── rate_limit.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── billing/                        # Tariflar va subscription
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Plan, Subscription, MonthlyUsage
│   ├── serializers.py
│   ├── views.py                    # PlansView, MySubscriptionView
│   ├── urls.py                     # /api/billing/*
│   ├── services/
│   │   ├── __init__.py
│   │   ├── limits.py               # post limit check
│   │   └── subscriptions.py        # active plan logic
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── b2b/                            # B2B Lounge (post/feed)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # B2BProfile, B2BPost
│   ├── serializers.py
│   ├── views.py                    # feed, create, update, delete
│   ├── urls.py                     # /api/b2b/*
│   ├── permissions.py              # is_owner, is_b2b_enabled
│   ├── services/
│   │   ├── __init__.py
│   │   └── posts.py                # post create logic (billing check)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── chat/                           # Chat system
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # ChatThread, ChatMessage
│   ├── serializers.py
│   ├── views.py                    # start, threads, messages, send
│   ├── urls.py                     # /api/chat/*
│   ├── permissions.py              # is_participant
│   ├── services/
│   │   ├── __init__.py
│   │   └── messaging.py            # message create + notify
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── notifications/                  # Notifications
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Notification
│   ├── serializers.py
│   ├── views.py                    # list, read, read-all
│   ├── urls.py                     # /api/notifications/*
│   ├── services/
│   │   ├── __init__.py
│   │   └── notify.py               # create notification
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── common/                         # Shared utilities (ixtiyoriy)
│   ├── __init__.py
│   ├── permissions.py
│   ├── pagination.py
│   └── utils.py
│
└── static/                         # collectstatic output (prod)

```

## 🧠 Umumiy arxitektura

Frontend  
↓ (REST API + JWT)  
Backend (Django + DRF)  
↓  
Database (SQLite dev / Postgres prod)

Backend **faqat API** beradi. UI yo‘q.

---

## 📂 Modul tushuntirishi

### accounts/ — Auth & User
Telefon raqam asosida ishlaydi.
- OTP so‘rash
- OTP tasdiqlash
- Parol o‘rnatish / tiklash
- JWT token berish
- /me endpoint

### billing/ — Tarif va limitlar
- Plan: basic / pro / premium
- Subscription: user → plan
- MonthlyUsage: oy bo‘yicha post limiti

### b2b/ — B2B Lounge
- E’lon (feed) tizimi
- Admin tomonidan B2B yoqilishi shart
- Post yaratishda billing limit tekshiriladi

### chat/ — Chat
- Post asosida buyer ↔ seller suhbat
- Faqat ishtirokchilar ko‘ra oladi

### notifications/ — Notification
- DB-based notification
- Yangi xabar kelganda yaratiladi

---

## ⚙️ Local setup (Development)

### 1️⃣ Paketlarni o‘rnatish
```
python -m pip install -r requirements.txt
```

### 2️⃣ .env fayl

```
DEBUG=1  
SECRET_KEY=dev-secret-very-long-random-string  
ALLOWED_HOSTS=127.0.0.1,localhost  
CORS_ALLOWED_ORIGINS=http://localhost:3000  
DEV_OTP=1  
```

### 3️⃣ Migration
```
python manage.py migrate
```

### 4️⃣ Admin user
```
python manage.py createsuperuser
```

### 5️⃣ Server
```
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/

---

## 🛠 Admin panel — majburiy setup
1) Billing → Plans (basic, pro, premium)  
2) B2B → B2B Profiles → is_enabled = true  
3) Billing → Subscriptions → status = active  

---

## 🔐 Auth flow (Frontend uchun)

### OTP so‘rash
POST /api/auth/request-otp/

### OTP tasdiqlash
POST /api/auth/verify-otp/

### Parol o‘rnatish + token
POST /api/auth/set-password/

Header:
Authorization: Bearer <ACCESS_TOKEN>

---

## 🌐 Asosiy API endpointlar

Auth:
- POST /api/auth/request-otp/
- POST /api/auth/verify-otp/
- POST /api/auth/set-password/
- GET  /api/auth/me/

Billing:
- GET /api/billing/plans/
- GET /api/billing/me/

B2B:
- GET  /api/b2b/posts/
- POST /api/b2b/posts/

Chat:
- POST /api/chat/start/
- GET  /api/chat/threads/
- POST /api/chat/send/

Notifications:
- GET  /api/notifications/
- POST /api/notifications/read/

---

## 🚀 Production (Render)
```
DEBUG=0  
SECRET_KEY=long-random-secret  
ALLOWED_HOSTS=your-app.onrender.com  
DATABASE_URL=postgres://...  
DEV_OTP=0  
```

---
### 🔐 AUTH: Frontend ulash uchun asosiy qoida

**Base URL**

1) Local: http://127.0.0.1:8000

2) Prod: [https://<your-service>.onrender.com](https://<your-service>.onrender.com)

**Frontend request’lari:**
```
POST/GET ${BASE_URL}/api/...
```

**JWT header (protected endpointlar)**

```
Authorization: Bearer <ACCESS_TOKEN>
```

