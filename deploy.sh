#!/bin/bash
set -e

echo "================================================"
echo "  DIACO MES - Deployment Started"
echo "  https://diaco.iranianc.com"
echo "================================================"

PROJECT_DIR="/home/diaco761/public_html"
PYTHON="$PROJECT_DIR/venv/bin/python3"
PIP="$PROJECT_DIR/venv/bin/pip"

cd $PROJECT_DIR

echo ""
echo "[1/5] Pulling latest code..."
git pull origin main

echo ""
echo "[2/5] Installing requirements..."
$PIP install -r requirements.txt -q

echo ""
echo "[3/5] Collecting static files..."
$PYTHON manage.py collectstatic --noinput --settings=config.settings.production

echo ""
echo "[4/5] Running migrations..."
$PYTHON manage.py migrate --settings=config.settings.production

echo ""
echo "[5/5] Restarting Passenger..."
mkdir -p tmp && touch tmp/restart.txt

echo ""
echo "================================================"
echo "  SUCCESS - https://diaco.iranianc.com"
echo "================================================"
