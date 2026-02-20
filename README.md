# دیاکو MES — سیستم مدیریت تولید

**Diaco Manufacturing Execution System**  
شرکت توسعه هوشمند فرش ایرانیان | پارک علم و فناوری کاشان

---

## معرفی

دیاکو MES یک سیستم جامع مدیریت اجرای تولید برای صنعت نساجی (ریسندگی نخ فرش) است که با Django 4.2 توسعه یافته است.

## قابلیت‌ها

- مدیریت خطوط تولید (حلاجی، کاردینگ، پاساژ، فینیشر، رینگ)
- تکمیل نخ v2.0 (بوبین‌پیچی WD، دولاتابی TFO، هیت‌ست HS)
- مانیتورینگ زنده خطوط تولید و نقشه Heatmap کارگاه
- مدیریت سفارشات و مشتریان
- انبار مواد اولیه (الیاف، رنگ، مواد شیمیایی)
- سیستم نگهداری و تعمیرات (PM، WO، لاگ توقفات)
- گزارش‌گیری جامع با تقویم شمسی
- رابط تبلت برای اپراتورهای خط تولید
- پشتیبانی کامل RTL و زبان فارسی

## پشته فناوری

- **Backend:** Django 4.2 LTS + Django REST Framework
- **Database:** MySQL / MariaDB
- **Frontend:** Bootstrap 5 RTL (Kayo Admin) + Vazirmatn
- **Icons:** Tabler Icons
- **Charts:** ApexCharts
- **Calendar:** django-jalali + JalaliDatePicker

## نصب و راه‌اندازی

```bash
# ۱. clone
git clone git@github.com:itwman/Diaco.git
cd Diaco

# ۲. محیط مجازی
python -m venv venv
venv\Scripts\activate   # Windows

# ۳. نصب وابستگی‌ها
pip install -r requirements.txt

# ۴. تنظیمات محیطی
copy .env.example .env
# فایل .env را ویرایش کنید

# ۵. migration
python manage.py migrate

# ۶. superuser
python manage.py createsuperuser

# ۷. اجرا
python manage.py runserver
```

## ساختار پروژه

```
Diaco/
├── apps/           ← اپلیکیشن‌های Django
│   ├── core/       ← خطوط و ماشین‌آلات
│   ├── accounts/   ← احراز هویت
│   ├── inventory/  ← انبار
│   ├── orders/     ← سفارشات
│   ├── blowroom/   ← حلاجی
│   ├── carding/    ← کاردینگ
│   ├── passage/    ← پاساژ
│   ├── finisher/   ← فینیشر
│   ├── spinning/   ← رینگ
│   ├── winding/    ← بوبین‌پیچی (v2.0)
│   ├── tfo/        ← دولاتابی (v2.0)
│   ├── heatset/    ← هیت‌ست (v2.0)
│   ├── dyeing/     ← رنگرزی
│   ├── maintenance/← نگهداری
│   ├── dashboard/  ← داشبورد
│   ├── reports/    ← گزارش‌ها
│   └── ai_ready/   ← آماده‌سازی AI
├── config/         ← تنظیمات Django
├── templates/      ← قالب‌های HTML
├── RTL/assets/     ← فایل‌های استاتیک
└── docs/           ← مستندات
```

## مستندات

- [نقشه راه توسعه](docs/ROADMAP.md)
- [ERD پایگاه داده](docs/02_COMPLETE_ERD.md)

---

© ۱۴۰۴ شرکت توسعه هوشمند فرش ایرانیان
