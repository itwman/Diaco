#!/bin/bash
# ================================================
#  DIACO MES — Deploy Script
#  سرور: diaco.iranianc.com (Chabokan)
#  اجرا روی سرور: bash deploy.sh
# ================================================

set -e  # خروج فوری در صورت خطا

echo "================================================"
echo "  DIACO MES - Deployment Started"
echo "================================================"

PROJECT_DIR="/home/diaco761/public_html"
PYTHON="$PROJECT_DIR/venv/bin/python3"
PIP="$PROJECT_DIR/venv/bin/pip"

cd $PROJECT_DIR

# ─── Step 1: دریافت آخرین کد ─────────────────────
echo ""
echo "[1/6] Pulling latest code from GitHub..."
git pull origin main

# ─── Step 2: نصب وابستگی‌ها ──────────────────────
echo ""
echo "[2/6] Installing/updating requirements..."
$PIP install -r requirements.txt --quiet

# ─── Step 3: collectstatic ───────────────────────
echo ""
echo "[3/6] Collecting static files..."
$PYTHON manage.py collectstatic --noinput --settings=config.settings.production

# ─── Step 4: migration ───────────────────────────
echo ""
echo "[4/6] Running migrations..."
$PYTHON manage.py migrate --settings=config.settings.production

# ─── Step 5: بررسی ───────────────────────────────
echo ""
echo "[5/6] Checking deployment..."
$PYTHON manage.py check --deploy --settings=config.settings.production 2>&1 | grep -v "^System check" || true

# ─── Step 6: restart Passenger ───────────────────
echo ""
echo "[6/6] Restarting application..."
mkdir -p tmp
touch tmp/restart.txt

echo ""
echo "================================================"
echo "  SUCCESS - Deployment Complete!"
echo "  https://diaco.iranianc.com"
echo "================================================"
