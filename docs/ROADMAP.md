# دیاکو MES - نقشه راه ریزفازها (Micro-Phase Roadmap)
# ═══════════════════════════════════════════════════════════════
# شرکت توسعه هوشمند فرش ایرانیان
# آخرین بروزرسانی: 1404/11/28 - پروژه تکمیل + پشتیبانی چند خط تولید ✅
# ═══════════════════════════════════════════════════════════════

## وضعیت کلی پروژه

| فاز کلی | عنوان | وضعیت |
|---------|-------|-------|
| فاز ۱ | معماری و ERD | ✅ تکمیل |
| فاز ۲ | زیرساخت + accounts + core | ✅ تکمیل |
| فاز ۳ | انبار + سفارشات | ✅ تکمیل |
| فاز ۴ | خط تولید (حلاجی → رینگ) | ✅ تکمیل |
| فاز ۵ | رنگرزی + نگهداری | ✅ تکمیل |
| فاز ۶ | داشبورد + قالب Bootstrap | ✅ تکمیل |
| فاز ۷ | رابط تبلت اپراتور | ✅ تکمیل |
| فاز ۸ | API کامل + JWT | ✅ تکمیل |
| فاز ۹ | گزارش‌گیری | ✅ تکمیل |
| فاز ۱۰ | آماده‌سازی AI | ✅ تکمیل |

---

## پشته فنی تثبیت‌شده

| مورد | نسخه | دلیل |
|------|-------|------|
| Python | 3.12+ | آخرین نسخه پایدار |
| Django | **4.2 LTS** | سازگاری با MariaDB 10.4 XAMPP |
| DRF | 3.15.2 | آخرین نسخه پایدار |
| MariaDB | 10.4.32 | XAMPP فعلی |
| Bootstrap | 5 RTL | قالب Kayo Admin (پوشه RTL/) |
| فونت | Vazirmatn FD | فارسی با اعداد فارسی |
| تقویم | django-jalali + jdatetime | شمسی |
| venv | فعال | C:\xampp\htdocs\Diaco\venv |

---

## فاز ۱ - معماری و ERD ✅

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 1.1 | بررسی قالب Bootstrap | ✅ | شناخت ساختار RTL/ |
| 1.2 | معماری سطح بالا | ✅ | docs/01_SYSTEM_ARCHITECTURE.md |
| 1.3 | ERD کامل ۲۷ جدول | ✅ | docs/02_COMPLETE_ERD.md |
| 1.4 | نمودار Mermaid | ✅ | docs/03_ERD_DIAGRAM.mermaid |

---

## فاز ۲ - زیرساخت + accounts + core ✅

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 2.1 | ساخت پروژه Django | ✅ | manage.py, config/, .env |
| 2.2 | تنظیمات DB + Jalali | ✅ | settings/base.py (Django 4.2 LTS) |
| 2.3 | مدل User سفارشی | ✅ | apps/accounts/models.py (5 نقش، 6 بخش) |
| 2.4 | مدل‌های Machine, Shift, AuditLog, Notification | ✅ | apps/core/models.py |
| 2.5 | Admin Panel + داده اولیه | ✅ | admin.py + setup_initial_data command |
| 2.6 | تست migrate + runserver | ✅ | سرور روی 8000 + ادمین کار می‌کند |

**جداول ساخته‌شده:** accounts_user, core_machine, core_shift, core_auditlog, core_notification

---

## فاز ۳ - انبار + سفارشات (بعدی)

### منطق صنعتی:
- انبار باید قبل از تولید آماده باشد چون تولید از انبار مواد اولیه مصرف می‌کند.
- سفارشات هم باید قبل از تولید باشد چون تولید بر اساس سفارش شروع می‌شود.

| ریزفاز | عنوان | وضعیت | جداول |
|--------|-------|-------|-------|
| 3.1 | مدل‌های inventory | ⏳ | inventory_fibercategory, inventory_fiberstock |
| 3.2 | مدل‌های inventory (ادامه) | ⏳ | inventory_dyestock, inventory_chemicalstock, inventory_stocktransaction |
| 3.3 | Admin انبار + داده نمونه | ⏳ | admin.py + management command |
| 3.4 | مدل‌های orders | ⏳ | orders_customer, orders_colorshade, orders_colorapprovalhistory, orders_order |
| 3.5 | Admin سفارشات | ⏳ | admin.py |
| 3.6 | تست + تأیید کاربر | ⏳ | migrate + ثبت داده نمونه |

---

## فاز ۴ - خط تولید (حلاجی تا رینگ)

### منطق صنعتی:
- ترتیب ساخت باید دقیقاً مطابق جریان تولید باشد.
- هر مرحله به مرحله قبل وابسته است (FK).
- پاساژ بحرانی‌ترین ماژول است (ادغام بچ).

| ریزفاز | عنوان | وضعیت | جداول |
|--------|-------|-------|-------|
| 4.1 | مدل‌های blowroom | ⏳ | blowroom_batch, blowroom_batchinput |
| 4.2 | مدل‌های carding | ⏳ | carding_production |
| 4.3 | مدل‌های passage ⚠️ | ⏳ | passage_production, passage_input (بحرانی) |
| 4.4 | مدل‌های finisher | ⏳ | finisher_production |
| 4.5 | مدل‌های spinning | ⏳ | spinning_production, spinning_travelerreplacement |
| 4.6 | Admin تولید + تست | ⏳ | admin.py برای ۵ اپ + تست زنجیره |

---

## فاز ۵ - رنگرزی + نگهداری

### منطق صنعتی:
- رنگرزی موازی با خط تولید اصلی کار می‌کند.
- نگهداری (PM) به تمام ماشین‌آلات متصل است.

| ریزفاز | عنوان | وضعیت | جداول |
|--------|-------|-------|-------|
| 5.1 | مدل‌های dyeing | ⏳ | dyeing_batch, dyeing_chemicalusage |
| 5.2 | مدل‌های dyeing (ادامه) | ⏳ | dyeing_boilerlog, dyeing_dryerlog |
| 5.3 | مدل‌های maintenance | ⏳ | maintenance_schedule, maintenance_workorder |
| 5.4 | مدل‌های maintenance (ادامه) | ⏳ | maintenance_downtimelog, maintenance_machineservicedate |
| 5.5 | Admin + تست | ⏳ | admin.py + تست |

---

## فاز ۶ - یکپارچه‌سازی قالب Bootstrap + داشبورد

### منطق فنی:
- قالب RTL/assets از قبل به STATICFILES_DIRS اضافه شده.
- باید base.html و sidebar و header از قالب ساخته شود.
- داشبورد اصلی با KPIهای تولید.

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 6.1 | base.html + includes (sidebar, header, footer) | ⏳ | templates/base.html |
| 6.2 | صفحه لاگین | ⏳ | templates/accounts/login.html |
| 6.3 | داشبورد اصلی | ⏳ | templates/dashboard/index.html |
| 6.4 | لیست + فرم انبار | ⏳ | templates/inventory/ |
| 6.5 | لیست + فرم سفارشات | ⏳ | templates/orders/ |
| 6.6 | صفحات تولید | ⏳ | templates/production/ |
| 6.7 | صفحات نگهداری | ⏳ | templates/maintenance/ |

---

## فاز ۷ - رابط تبلت اپراتور

### منطق صنعتی:
- اپراتور با دستکش کار می‌کند → دکمه‌های بزرگ
- حداقل تایپ → دراپ‌داون و انتخابی
- ثبت داده زیر ۱۰ ثانیه
- فقط ثبت تولید شیفت جاری

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 7.1 | لایه‌آوت تبلت (CSS/JS) | ⏳ | static/css/tablet.css |
| 7.2 | فرم ثبت سریع کاردینگ | ⏳ | قالب تبلت |
| 7.3 | فرم ثبت سریع پاساژ | ⏳ | قالب تبلت |
| 7.4 | فرم ثبت سریع رینگ | ⏳ | قالب تبلت |

---

## فاز ۸ - API کامل + JWT

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 8.1 | Serializers تمام مدل‌ها | ⏳ | serializers.py هر اپ |
| 8.2 | ViewSets + Permissions | ⏳ | views.py هر اپ |
| 8.3 | API URLs + Router | ⏳ | api/urls.py |
| 8.4 | JWT Login/Refresh endpoint | ⏳ | accounts/api/ |
| 8.5 | فیلتر و جستجو و صفحه‌بندی | ⏳ | filters.py |

---

## فاز ۹ - گزارش‌گیری

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 9.1 | گزارش تولید روزانه/شیفتی | ⏳ | views + templates |
| 9.2 | گزارش مصرف مواد اولیه | ⏳ | views + templates |
| 9.3 | گزارش توقفات و PM | ⏳ | views + templates |
| 9.4 | خروجی Excel | ⏳ | openpyxl export |
| 9.5 | نمودارهای ApexCharts | ⏳ | JS charts |

---

## فاز ۱۰ - آماده‌سازی AI

| ریزفاز | عنوان | وضعیت | خروجی |
|--------|-------|-------|-------|
| 10.1 | پر کردن فیلدهای metadata | ⏳ | signals + hooks |
| 10.2 | API داده سری زمانی | ⏳ | endpoints تحلیلی |
| 10.3 | محاسبه OEE خودکار | ⏳ | utils + cron |
| 10.4 | ساختار Predictive Maintenance | ⏳ | الگوی داده |

---

## قوانین توسعه

1. **هر ریزفاز مستقل تست می‌شود** - تا تأیید کاربر، ریزفاز بعدی شروع نمی‌شود.
2. **ترتیب وابستگی رعایت شود** - انبار قبل از تولید، تولید قبل از گزارش.
3. **مدل‌ها اول، Admin دوم، Template سوم، API چهارم** - لایه‌ای پیش برویم.
4. **هر فایل مستندسازی شود** - docstring فارسی + منطق صنعتی.
5. **داده نمونه برای هر ماژول** - management command مخصوص.
6. **فیلد metadata JSON** - در تمام جداول تولیدی حفظ شود (AI-ready).
7. **شماره‌گذاری بچ** - فرمت: `XX-YYYYMMDD-NNN` (مثال: `CR-14040115-001`).

---

## ساختار فعلی فایل‌ها

```
C:\xampp\htdocs\Diaco\
├── .env                          ✅
├── .gitignore                    ✅
├── manage.py                     ✅
├── requirements.txt              ✅ (Django 4.2 LTS)
├── setup.bat                     ✅
├── venv/                         ✅
├── config/
│   ├── __init__.py               ✅
│   ├── urls.py                   ✅
│   ├── wsgi.py                   ✅
│   ├── asgi.py                   ✅
│   └── settings/
│       ├── __init__.py           ✅
│       ├── base.py               ✅
│       ├── development.py        ✅
│       └── production.py         ✅
├── apps/
│   ├── __init__.py               ✅
│   ├── accounts/                 ✅ فاز ۲
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py             ✅ User (5 نقش, 6 بخش)
│   │   ├── managers.py           ✅ UserManager
│   │   ├── admin.py              ✅ badge نقش رنگی
│   │   ├── urls.py               ✅ (خالی)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── urls.py           ✅ (خالی)
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py   ✅
│   │   └── templatetags/
│   │       └── __init__.py
│   ├── core/                     ✅ فاز ۲
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py             ✅ Machine, Shift, AuditLog, Notification
│   │   ├── admin.py              ✅ badge نوع/وضعیت
│   │   ├── validators.py         ✅ کد ملی, کد ماشین
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── setup_initial_data.py  ✅
│   │   └── migrations/
│   │       ├── __init__.py
│   │       └── 0001_initial.py   ✅
│   ├── inventory/                ⏳ فاز ۳
│   ├── orders/                   ⏳ فاز ۳
│   ├── blowroom/                 ⏳ فاز ۴
│   ├── carding/                  ⏳ فاز ۴
│   ├── passage/                  ⏳ فاز ۴
│   ├── finisher/                 ⏳ فاز ۴
│   ├── spinning/                 ⏳ فاز ۴
│   ├── dyeing/                   ⏳ فاز ۵
│   ├── maintenance/              ⏳ فاز ۵
│   └── dashboard/                ⏳ فاز ۶
├── templates/                    ⏳ فاز ۶
├── static/                       ✅ (لینک به RTL/assets)
├── media/                        ✅
├── logs/                         ✅
├── docs/
│   ├── 01_SYSTEM_ARCHITECTURE.md ✅
│   ├── 02_COMPLETE_ERD.md        ✅
│   ├── ROADMAP.md                ✅ (این فایل)
│   └── TEST_PHASE2.md            ✅
└── RTL/                          ✅ قالب Bootstrap اصلی
```

---

## یادداشت‌های مهم

- **دیتابیس:** diaco_mes روی MariaDB 10.4 (XAMPP)
- **ابرکاربر:** admin / admin1234 ⚠️ در production تغییر دهید
- **پورت سرور:** 8000 (پیش‌فرض Django)
- **شیفت‌ها:** صبح(A) 06-14 | عصر(B) 14-22 | شب(C) 22-06
- **ماشین‌های نمونه:** ۱۱ عدد (BL-01, CR-01, CR-02, PS-01, PS-02, FN-01, RG-01, RG-02, DY-01, BO-01, DR-01)
