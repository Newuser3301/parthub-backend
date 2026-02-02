#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting build process..."

# 1. Python paketlarni o‘rnatish
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 2. Static fayllarni yig‘ish (agar bo‘lsa)
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 3. Database migrate
echo "🗄️ Applying database migrations..."
python manage.py migrate

echo "✅ Build finished successfully!"

