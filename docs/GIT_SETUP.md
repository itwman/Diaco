# راهنمای دستی Git — دیاکو MES

## پیش‌نیاز: بررسی SSH Key

قبل از اجرا، مطمئن شوید SSH key دارید:

```cmd
# بررسی وجود key
dir %USERPROFILE%\.ssh\id_*.pub

# اگر نداشتید بسازید:
ssh-keygen -t ed25519 -C "dev@diaco-mes.ir"

# public key را کپی کنید:
type %USERPROFILE%\.ssh\id_ed25519.pub

# این مقدار را به GitHub اضافه کنید:
# GitHub → Settings → SSH and GPG keys → New SSH key
```

## تست اتصال به GitHub

```cmd
ssh -T git@github.com
# پیام موفقیت: Hi itwman! You've successfully authenticated...
```

---

## روش ۱: اسکریپت خودکار (توصیه می‌شود)

```cmd
cd C:\xampp\htdocs\Diaco
git_init.bat
```

---

## روش ۲: دستی (اگر اسکریپت کار نکرد)

```cmd
cd C:\xampp\htdocs\Diaco

REM مرحله ۱: init
git init

REM مرحله ۲: identity
git config user.name "Diaco MES"
git config user.email "dev@diaco-mes.ir"

REM مرحله ۳: بررسی فایل‌های ignored
git status

REM مرحله ۴: add همه چیز
git add .

REM مرحله ۵: بررسی دوباره
git status --short

REM مرحله ۶: commit
git commit -m "feat: initial commit — Diaco MES v1.0"

REM مرحله ۷: branch + remote + push
git branch -M main
git remote add origin git@github.com:itwman/Diaco.git
git push -u origin main
```

---

## بررسی حجم قبل از push

```cmd
REM چه چیزی push می‌شود:
git status
git diff --cached --stat

REM حجم کل tracked files:
git ls-files | measure-object  (PowerShell)
```

---

## بعد از موفقیت

```cmd
REM مشاهده log
git log --oneline

REM مشاهده remotes
git remote -v

REM آدرس مخزن:
REM https://github.com/itwman/Diaco
```

---

## دستورات روزمره (بعد از setup)

```cmd
REM وضعیت تغییرات
git status

REM افزودن و commit
git add .
git commit -m "feat: توضیح تغییر"

REM push
git push

REM pull (هنگام کار روی سرور)
git pull origin main
```
