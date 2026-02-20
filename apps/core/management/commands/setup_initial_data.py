"""
Diaco MES - Setup Initial Data
================================
ساخت داده‌های اولیه: شیفت‌ها + ابرکاربر + ماشین‌های نمونه.

Usage:
    python manage.py setup_initial_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Shift, Machine

User = get_user_model()


class Command(BaseCommand):
    help = 'ساخت داده‌های اولیه دیاکو: شیفت‌ها، ابرکاربر و ماشین‌های نمونه'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n═══ دیاکو MES - راه‌اندازی اولیه ═══\n'))

        self._create_shifts()
        self._create_superuser()
        self._create_sample_machines()

        self.stdout.write(self.style.SUCCESS('\n✅ راه‌اندازی اولیه با موفقیت انجام شد!\n'))

    def _create_shifts(self):
        """ساخت ۳ شیفت استاندارد"""
        shifts_data = [
            {'name': 'صبح', 'code': 'A', 'start_time': '06:00', 'end_time': '14:00'},
            {'name': 'عصر', 'code': 'B', 'start_time': '14:00', 'end_time': '22:00'},
            {'name': 'شب', 'code': 'C', 'start_time': '22:00', 'end_time': '06:00'},
        ]

        for data in shifts_data:
            shift, created = Shift.objects.get_or_create(
                code=data['code'],
                defaults=data,
            )
            if created:
                self.stdout.write(f'  ✓ شیفت «{shift.name}» ایجاد شد')
            else:
                self.stdout.write(f'  - شیفت «{shift.name}» از قبل وجود دارد')

    def _create_superuser(self):
        """ساخت ابرکاربر پیش‌فرض"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin1234',
                first_name='مدیر',
                last_name='سیستم',
                role='admin',
                department='office',
            )
            self.stdout.write(self.style.WARNING(
                '  ✓ ابرکاربر «admin» ایجاد شد (رمز: admin1234)'
            ))
            self.stdout.write(self.style.WARNING(
                '    ⚠️  حتماً رمز عبور را در محیط تولید تغییر دهید!'
            ))
        else:
            self.stdout.write('  - ابرکاربر «admin» از قبل وجود دارد')

    def _create_sample_machines(self):
        """ساخت چند ماشین نمونه"""
        machines_data = [
            {'code': 'BL-01', 'name': 'حلاجی شماره ۱', 'machine_type': 'blowroom', 'location': 'سالن الف'},
            {'code': 'CR-01', 'name': 'کارد شماره ۱', 'machine_type': 'carding', 'location': 'سالن الف'},
            {'code': 'CR-02', 'name': 'کارد شماره ۲', 'machine_type': 'carding', 'location': 'سالن الف'},
            {'code': 'PS-01', 'name': 'پاساژ شماره ۱', 'machine_type': 'passage', 'location': 'سالن ب'},
            {'code': 'PS-02', 'name': 'پاساژ شماره ۲', 'machine_type': 'passage', 'location': 'سالن ب'},
            {'code': 'FN-01', 'name': 'فینیشر شماره ۱', 'machine_type': 'finisher', 'location': 'سالن ب'},
            {'code': 'RG-01', 'name': 'رینگ شماره ۱', 'machine_type': 'ring', 'location': 'سالن ج'},
            {'code': 'RG-02', 'name': 'رینگ شماره ۲', 'machine_type': 'ring', 'location': 'سالن ج'},
            # ── v2.0: خط تولید نخ فرش ────────────────────────
            {'code': 'WD-01', 'name': 'بوبین‌پیچ شماره ۱', 'machine_type': 'winding', 'location': 'سالن تکمیل'},
            {'code': 'WD-02', 'name': 'بوبین‌پیچ شماره ۲', 'machine_type': 'winding', 'location': 'سالن تکمیل'},
            {'code': 'TFO-01', 'name': 'دولاتاب TFO شماره ۱', 'machine_type': 'tfo', 'location': 'سالن تکمیل'},
            {'code': 'TFO-02', 'name': 'دولاتاب TFO شماره ۲', 'machine_type': 'tfo', 'location': 'سالن تکمیل'},
            {'code': 'HS-01', 'name': 'اتوکلاو هیت‌ست شماره ۱', 'machine_type': 'heatset', 'location': 'سالن تکمیل'},
            # ────────────────────────────────────────────────────
            {'code': 'DY-01', 'name': 'دیگ رنگرزی ۱', 'machine_type': 'dyeing', 'location': 'سالن رنگرزی'},
            {'code': 'BO-01', 'name': 'دیگ بخار ۱', 'machine_type': 'boiler', 'location': 'موتورخانه'},
            {'code': 'DR-01', 'name': 'خشک‌کن ۱', 'machine_type': 'dryer', 'location': 'سالن رنگرزی'},
        ]

        for data in machines_data:
            machine, created = Machine.objects.get_or_create(
                code=data['code'],
                defaults=data,
            )
            if created:
                self.stdout.write(f'  ✓ ماشین «{machine.code} - {machine.name}» ایجاد شد')
            else:
                self.stdout.write(f'  - ماشین «{machine.code}» از قبل وجود دارد')
