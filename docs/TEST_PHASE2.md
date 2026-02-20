# دیاکو MES - راهنمای تست ریزفاز ۲
## اپلیکیشن accounts و core

### پیش‌نیازها

1. **Python 3.12+** نصب باشد
2. **MySQL 8** روی XAMPP اجرا باشد
3. دیتابیس `diaco_mes` در MySQL ساخته شود

---

### مرحله ۱: ساخت دیتابیس MySQL

MySQL shell یا phpMyAdmin را باز کنید و اجرا کنید:

```sql
CREATE DATABASE diaco_mes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### مرحله ۲: نصب وابستگی‌ها

```cmd
cd C:\xampp\htdocs\Diaco
pip install -r requirements.txt
```

---

### مرحله ۳: اجرای مهاجرت

```cmd
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py migrate
```

خروجی مورد انتظار: ساخت جداول بدون خطا.

---

### مرحله ۴: داده‌های اولیه

```cmd
python manage.py setup_initial_data
```

خروجی مورد انتظار:
```
═══ دیاکو MES - راه‌اندازی اولیه ═══

  ✓ شیفت «صبح» ایجاد شد
  ✓ شیفت «عصر» ایجاد شد
  ✓ شیفت «شب» ایجاد شد
  ✓ ابرکاربر «admin» ایجاد شد (رمز: admin1234)
  ✓ ماشین «BL-01 - حلاجی شماره ۱» ایجاد شد
  ...

✅ راه‌اندازی اولیه با موفقیت انجام شد!
```

---

### مرحله ۵: اجرای سرور

```cmd
python manage.py runserver
```

---

### مرحله ۶: تست پنل مدیریت

1. مرورگر را باز کنید: **http://127.0.0.1:8000/admin/**
2. با نام کاربری `admin` و رمز `admin1234` وارد شوید

باید ببینید:
- **مدیریت کاربران** → کاربران (۱ رکورد: مدیر سیستم)
- **هسته سیستم** → ماشین‌آلات (۱۱ رکورد)
- **هسته سیستم** → شیفت‌ها (۳ رکورد: صبح/عصر/شب)
- **هسته سیستم** → لاگ تغییرات (خالی)
- **هسته سیستم** → اعلان‌ها (خالی)

---

### مرحله ۷: تست ساخت کاربر جدید

در پنل ادمین:
1. روی «کاربران» → «افزودن کاربر» کلیک کنید
2. نام کاربری: `operator1`
3. رمز عبور: `test1234`
4. نام: `علی` | نام خانوادگی: `محمدی`
5. نقش: `اپراتور` | بخش: `تولید`
6. ذخیره کنید

---

### چک‌لیست تست

- [ ] دیتابیس بدون خطا ساخته شد
- [ ] مهاجرت بدون خطا اجرا شد
- [ ] داده‌های اولیه بدون خطا ساخته شدند
- [ ] پنل ادمین باز می‌شود
- [ ] لاگین با admin/admin1234 کار می‌کند
- [ ] ماشین‌آلات نمایش داده می‌شوند (badge رنگی نوع و وضعیت)
- [ ] شیفت‌ها نمایش داده می‌شوند
- [ ] ساخت کاربر جدید کار می‌کند
- [ ] فیلترها (نقش، بخش، نوع ماشین) کار می‌کنند

---

### ساختار جداول ساخته شده

| جدول | فیلدهای کلیدی |
|------|--------------|
| `accounts_user` | username, role, department, national_code |
| `core_machine` | code, machine_type, status, specs(JSON) |
| `core_shift` | code, name, start_time, end_time |
| `core_auditlog` | user, action, table_name, old/new_values(JSON) |
| `core_notification` | recipient, title, notif_type, is_read |

---

**بعد از تست موفق، پیام بدهید تا ریزفاز بعدی (inventory + orders) شروع شود.**
