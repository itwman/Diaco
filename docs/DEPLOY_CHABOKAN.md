# راهنمای انتقال دیاکو MES به سرور چابکان
**آدرس:** diaco.iranianc.com

---

## پیش‌نیازها (پنل چابکان)

قبل از شروع، در پنل چابکان بررسی کنید:
- Python 3.11 فعال باشد (Python App)
- دسترسی SSH داشته باشید
- دیتابیس MySQL ساخته شده باشد

---

## مرحله ۱ — ورود به سرور از طریق SSH

```bash
# اطلاعات SSH از پنل چابکان بگیرید
ssh diaco761@diaco.iranianc.com
# یا با پورت مشخص:
ssh -p 22 diaco761@diaco.iranianc.com
```

---

## مرحله ۲ — clone پروژه

```bash
# رفتن به پوشه public_html
cd ~/public_html

# حذف فایل‌های پیش‌فرض (اگر وجود دارد)
rm -rf *

# clone از GitHub
git clone git@github.com:itwman/Diaco.git .
# نکته: نقطه آخر مهم است — داخل همین پوشه clone شود
```

---

## مرحله ۳ — محیط مجازی Python

```bash
cd ~/public_html

# ساخت venv
python3.11 -m venv venv

# فعال‌سازی
source venv/bin/activate

# نصب requirements
pip install -r requirements.txt
```

---

## مرحله ۴ — فایل .env

```bash
# کپی از نمونه
cp .env.production .env

# بررسی محتوا (باید صحیح باشد)
cat .env
```

محتوای `.env` باید این باشد:
```
SECRET_KEY=u#p3$k9@mz!qr7vx2ywn6jd4te8ls1oc0fb5ih_ga&diaco-prod-2024
DEBUG=False
ALLOWED_HOSTS=diaco.iranianc.com,www.diaco.iranianc.com
DB_NAME=diaco761_wayne
DB_USER=diaco761_wayne
DB_PASSWORD=zulexkTIUCob
DB_HOST=services.irn9.chabokan.net
DB_PORT=16584
CORS_ALLOWED_ORIGINS=https://diaco.iranianc.com
```

---

## مرحله ۵ — تست اتصال دیتابیس

```bash
source venv/bin/activate

python manage.py dbshell --settings=config.settings.production
# اگر وارد MySQL شد، اتصال برقرار است
# خروج: exit
```

---

## مرحله ۶ — Migration و Static

```bash
source venv/bin/activate

# ساخت جداول دیتابیس
python manage.py migrate --settings=config.settings.production

# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput --settings=config.settings.production

# ساخت superuser
python manage.py createsuperuser --settings=config.settings.production
```

---

## مرحله ۷ — تنظیم Python App در پنل چابکان

در پنل چابکان → Python App:

| فیلد | مقدار |
|------|-------|
| Python Version | 3.11 |
| Application root | public_html |
| Application URL | / |
| Application startup file | passenger_wsgi.py |
| Application Entry point | application |

---

## مرحله ۸ — بررسی نهایی

```bash
# تست Django
python manage.py check --deploy --settings=config.settings.production

# restart Passenger
mkdir -p tmp && touch tmp/restart.txt
```

سپس آدرس `https://diaco.iranianc.com` را در مرورگر باز کنید.

---

## عیب‌یابی

### خطای دیتابیس
```bash
# تست مستقیم اتصال MySQL
python -c "
import MySQLdb
conn = MySQLdb.connect(
    host='services.irn9.chabokan.net',
    port=16584,
    user='diaco761_wayne',
    passwd='zulexkTIUCob',
    db='diaco761_wayne'
)
print('DB Connection OK!')
conn.close()
"
```

### خطای static files
```bash
ls -la staticfiles/   # باید پر باشد
python manage.py collectstatic --noinput --settings=config.settings.production
```

### مشاهده لاگ خطا
```bash
tail -f logs/diaco.log
# یا لاگ Passenger:
tail -f ~/logs/passenger.log
```

### restart برنامه
```bash
touch tmp/restart.txt
```

---

## آپدیت در آینده

```bash
cd ~/public_html
bash deploy.sh
```

---

## اطلاعات دیتابیس

| فیلد | مقدار |
|------|-------|
| Host | services.irn9.chabokan.net |
| Port | 16584 |
| Database | diaco761_wayne |
| User | diaco761_wayne |
| Password | zulexkTIUCob |
