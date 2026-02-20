"""
Diaco MES - پر کردن کامل داده‌های تست
==========================================
ساخت ۳ خط تولید با تمام داده‌های مرتبط:
  - کاربران (مدیران، سرشیفت‌ها، اپراتورها، ناظران، تکنسین‌ها)
  - خطوط تولید + شیفت‌ها + اختصاص سرشیفت
  - ماشین‌آلات هر خط
  - انبار (الیاف، رنگ، شیمیایی)
  - مشتریان + شیدهای رنگی + سفارشات
  - بچ‌های تولید تمام مراحل (حلاجی→کاردینگ→پاساژ→فینیشر→رینگ)
  - رنگرزی + دیگ بخار + خشک‌کن
  - نگهداری (PM + WO + توقفات + سوابق سرویس)

Usage:
    python manage.py populate_full_data
    python manage.py populate_full_data --flush   (پاک‌سازی قبل از ساخت)
"""
import random
from datetime import date, time, timedelta, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.core.models import (
    ProductionLine, Machine, Shift, LineShiftAssignment,
    Notification,
)
from apps.inventory.models import (
    FiberCategory, FiberStock, DyeStock, ChemicalStock, StockTransaction,
)
from apps.orders.models import Customer, ColorShade, Order
from apps.blowroom.models import Batch as BlowroomBatch, BatchInput
from apps.carding.models import Production as CardingProduction
from apps.passage.models import Production as PassageProduction, Input as PassageInput
from apps.finisher.models import Production as FinisherProduction
from apps.spinning.models import Production as SpinningProduction, TravelerReplacement
from apps.dyeing.models import Batch as DyeingBatch, ChemicalUsage, BoilerLog, DryerLog
from apps.maintenance.models import Schedule, WorkOrder, DowntimeLog, MachineServiceDate

User = get_user_model()

# ═══════════════════════════════════════════════════════════════
# ثابت‌ها
# ═══════════════════════════════════════════════════════════════
TODAY = date.today()
NOW = datetime.now()

LINES_CONFIG = [
    {
        'code': 'LINE-01', 'name': 'خط یک - نخ پنبه‌ای',
        'product_type': 'نخ پنبه Ne30/1', 'capacity': 2000,
        'machines': {
            'blowroom': [('L1-BL-01', 'حلاجی خط ۱')],
            'carding': [('L1-CR-01', 'کارد ۱ خط ۱'), ('L1-CR-02', 'کارد ۲ خط ۱')],
            'passage': [('L1-PS-01', 'پاساژ ۱ خط ۱'), ('L1-PS-02', 'پاساژ ۲ خط ۱')],
            'finisher': [('L1-FN-01', 'فینیشر خط ۱')],
            'ring': [('L1-RG-01', 'رینگ ۱ خط ۱'), ('L1-RG-02', 'رینگ ۲ خط ۱')],
            'dyeing': [('L1-DY-01', 'دیگ رنگرزی خط ۱')],
            'boiler': [('L1-BO-01', 'دیگ بخار خط ۱')],
            'dryer': [('L1-DR-01', 'خشک‌کن خط ۱')],
        },
    },
    {
        'code': 'LINE-02', 'name': 'خط دو - نخ پلی‌استر',
        'product_type': 'نخ پلی‌استر Ne20/1', 'capacity': 2500,
        'machines': {
            'blowroom': [('L2-BL-01', 'حلاجی خط ۲')],
            'carding': [('L2-CR-01', 'کارد ۱ خط ۲'), ('L2-CR-02', 'کارد ۲ خط ۲')],
            'passage': [('L2-PS-01', 'پاساژ ۱ خط ۲')],
            'finisher': [('L2-FN-01', 'فینیشر خط ۲')],
            'ring': [('L2-RG-01', 'رینگ ۱ خط ۲'), ('L2-RG-02', 'رینگ ۲ خط ۲'), ('L2-RG-03', 'رینگ ۳ خط ۲')],
            'dyeing': [('L2-DY-01', 'دیگ رنگرزی خط ۲')],
            'boiler': [],
            'dryer': [('L2-DR-01', 'خشک‌کن خط ۲')],
        },
    },
    {
        'code': 'LINE-03', 'name': 'خط سه - نخ مخلوط',
        'product_type': 'نخ PES/VIS 70/30 Ne24/1', 'capacity': 1800,
        'machines': {
            'blowroom': [('L3-BL-01', 'حلاجی خط ۳')],
            'carding': [('L3-CR-01', 'کارد ۱ خط ۳')],
            'passage': [('L3-PS-01', 'پاساژ خط ۳')],
            'finisher': [('L3-FN-01', 'فینیشر خط ۳')],
            'ring': [('L3-RG-01', 'رینگ ۱ خط ۳'), ('L3-RG-02', 'رینگ ۲ خط ۳')],
            'dyeing': [('L3-DY-01', 'دیگ رنگرزی خط ۳')],
            'boiler': [],
            'dryer': [],
        },
    },
]

SUPERVISORS = [
    # (username, first, last, line_index)
    # هر خط ۳ سرشیفت (یکی برای هر شیفت)
    ('sup_l1_a', 'علی', 'محمدی', 0),
    ('sup_l1_b', 'حسن', 'رضایی', 0),
    ('sup_l1_c', 'محمد', 'کریمی', 0),
    ('sup_l2_a', 'رضا', 'احمدی', 1),
    ('sup_l2_b', 'مهدی', 'حسینی', 1),
    ('sup_l2_c', 'جواد', 'موسوی', 1),
    ('sup_l3_a', 'سعید', 'نوروزی', 2),
    ('sup_l3_b', 'امیر', 'قاسمی', 2),
    ('sup_l3_c', 'حمید', 'عباسی', 2),
]

OPERATORS = [
    ('op_01', 'ابراهیم', 'صادقی', 'production'),
    ('op_02', 'داود', 'فتحی', 'production'),
    ('op_03', 'یوسف', 'مرادی', 'production'),
    ('op_04', 'مجتبی', 'زمانی', 'production'),
    ('op_05', 'وحید', 'جعفری', 'production'),
    ('op_06', 'فرهاد', 'بهرامی', 'production'),
    ('op_07', 'کاظم', 'طاهری', 'dyeing'),
    ('op_08', 'ناصر', 'یزدانی', 'dyeing'),
    ('op_09', 'عباس', 'شریفی', 'maintenance'),
    ('op_10', 'منصور', 'رحیمی', 'maintenance'),
    ('op_11', 'اکبر', 'سلیمانی', 'production'),
    ('op_12', 'مسعود', 'دهقانی', 'production'),
]

FIBER_CATEGORIES = [
    ('PES', 'پلی‌استر', 'الیاف مصنوعی پلی‌استر'),
    ('VIS', 'ویسکوز', 'الیاف مصنوعی سلولزی'),
    ('COT', 'پنبه', 'الیاف طبیعی پنبه'),
    ('ACR', 'اکریلیک', 'الیاف اکریلیک'),
    ('WOL', 'پشم', 'الیاف طبیعی پشم'),
]

CUSTOMERS = [
    ('فرش ایران', 'شرکت فرش ایران', 'تهران', 'تهران', '09121111111'),
    ('نساجی اصفهان', 'شرکت نساجی اصفهان', 'اصفهان', 'اصفهان', '09132222222'),
    ('بافت کاشان', 'گروه بافت کاشان', 'کاشان', 'اصفهان', '09133333333'),
    ('تار و پود شرق', 'شرکت تار و پود شرق', 'مشهد', 'خراسان رضوی', '09154444444'),
    ('نخ ابریشم یزد', 'کارخانه نخ ابریشم یزد', 'یزد', 'یزد', '09135555555'),
]


class Command(BaseCommand):
    help = 'پر کردن کامل داده‌های تست برای ارزیابی سیستم دیاکو MES'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='حذف تمام داده‌های قبلی قبل از ساخت',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n╔══════════════════════════════════════════════╗\n'
            '║   دیاکو MES - پر کردن کامل داده‌های تست    ║\n'
            '╚══════════════════════════════════════════════╝\n'
        ))

        if options['flush']:
            self._flush_data()

        # ── ذخیره‌سازی مرجع ─────────────────────────────
        self.lines = []           # ProductionLine objects
        self.shifts = {}          # {line_code: {shift_code: Shift}}
        self.machines = {}        # {line_code: {type: [Machine]}}
        self.users = {}           # {username: User}
        self.fibers = []          # FiberStock objects
        self.dyes = []            # DyeStock objects
        self.chemicals = []       # ChemicalStock objects
        self.customers_obj = []   # Customer objects
        self.shades = []          # ColorShade objects
        self.orders_obj = []      # Order objects

        # ── مراحل ساخت ─────────────────────────────────
        self._step('۱', 'کاربران', self._create_users)
        self._step('۲', 'خطوط تولید + شیفت‌ها', self._create_lines_and_shifts)
        self._step('۳', 'ماشین‌آلات', self._create_machines)
        self._step('۴', 'اختصاص سرشیفت‌ها', self._create_shift_assignments)
        self._step('۵', 'انبار الیاف', self._create_fiber_inventory)
        self._step('۶', 'انبار رنگ و شیمیایی', self._create_dye_chemical_inventory)
        self._step('۷', 'مشتریان + شیدهای رنگی', self._create_customers_and_shades)
        self._step('۸', 'سفارشات', self._create_orders)
        self._step('۹', 'تولید حلاجی', self._create_blowroom_batches)
        self._step('۱۰', 'تولید کاردینگ', self._create_carding_productions)
        self._step('۱۱', 'تولید پاساژ', self._create_passage_productions)
        self._step('۱۲', 'تولید فینیشر', self._create_finisher_productions)
        self._step('۱۳', 'تولید رینگ', self._create_spinning_productions)
        self._step('۱۴', 'رنگرزی', self._create_dyeing_batches)
        self._step('۱۵', 'دیگ بخار و خشک‌کن', self._create_boiler_dryer_logs)
        self._step('۱۶', 'نگهداری (PM)', self._create_maintenance_schedules)
        self._step('۱۷', 'دستورهای کار', self._create_work_orders)
        self._step('۱۸', 'لاگ توقفات', self._create_downtime_logs)
        self._step('۱۹', 'اعلان‌ها', self._create_notifications)

        # ── خلاصه ────────────────────────────────────────
        self._print_summary()

    # ═══════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════

    def _step(self, num, title, func):
        self.stdout.write(f'\n── مرحله {num}: {title} ──')
        func()

    def _flush_data(self):
        self.stdout.write(self.style.WARNING('⚠️  پاک‌سازی داده‌های قبلی...'))
        for M in [
            Notification, DryerLog, BoilerLog, ChemicalUsage, DyeingBatch,
            TravelerReplacement, SpinningProduction, FinisherProduction,
            PassageInput, PassageProduction, CardingProduction,
            BatchInput, BlowroomBatch,
            DowntimeLog, MachineServiceDate, WorkOrder, Schedule,
            StockTransaction, Order,
            ChemicalStock, DyeStock, FiberStock, FiberCategory,
            Customer, ColorShade,
            LineShiftAssignment, Machine, Shift, ProductionLine,
        ]:
            cnt = M.objects.all().count()
            if cnt:
                M.objects.all().delete()
                self.stdout.write(f'  ✗ {M.__name__}: {cnt} رکورد حذف شد')
        # کاربران غیر admin
        del_count = User.objects.exclude(username='admin').count()
        if del_count:
            User.objects.exclude(username='admin').delete()
            self.stdout.write(f'  ✗ User: {del_count} کاربر حذف شد')

    # ═══════════════════════════════════════════════════════
    # ۱. کاربران
    # ═══════════════════════════════════════════════════════

    def _create_users(self):
        # ادمین
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'مدیر', 'last_name': 'سیستم',
                'role': 'admin', 'department': 'office',
                'is_staff': True, 'is_superuser': True,
            }
        )
        if not admin.has_usable_password():
            admin.set_password('admin1234')
            admin.save()
        self.users['admin'] = admin

        # مدیر تولید
        mgr, created = User.objects.get_or_create(
            username='manager01',
            defaults={
                'first_name': 'احمد', 'last_name': 'نیکخواه',
                'role': 'manager', 'department': 'production',
                'is_staff': True,
                'national_code': '1234567890',
                'phone': '09121234567',
            }
        )
        if created:
            mgr.set_password('pass1234')
            mgr.save()
        self.users['manager01'] = mgr
        self.stdout.write(f'  ✓ مدیر تولید: {mgr.get_full_name()}')

        # مدیر انبار
        wh, created = User.objects.get_or_create(
            username='warehouse01',
            defaults={
                'first_name': 'غلامرضا', 'last_name': 'توکلی',
                'role': 'manager', 'department': 'warehouse',
                'is_staff': True,
                'national_code': '1234567891',
            }
        )
        if created:
            wh.set_password('pass1234')
            wh.save()
        self.users['warehouse01'] = wh

        # مدیر نگهداری
        mt, created = User.objects.get_or_create(
            username='maint_mgr',
            defaults={
                'first_name': 'بهروز', 'last_name': 'فرجی',
                'role': 'manager', 'department': 'maintenance',
                'is_staff': True,
                'national_code': '1234567892',
            }
        )
        if created:
            mt.set_password('pass1234')
            mt.save()
        self.users['maint_mgr'] = mt

        # ناظر کیفیت
        qa, created = User.objects.get_or_create(
            username='qa_viewer',
            defaults={
                'first_name': 'زهرا', 'last_name': 'کاظمی',
                'role': 'viewer', 'department': 'quality',
                'national_code': '1234567893',
            }
        )
        if created:
            qa.set_password('pass1234')
            qa.save()
        self.users['qa_viewer'] = qa

        # سرشیفت‌ها (۹ نفر: ۳ خط × ۳ شیفت)
        nc = 1234567900
        for uname, fn, ln, _li in SUPERVISORS:
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': fn, 'last_name': ln,
                    'role': 'supervisor', 'department': 'production',
                    'national_code': str(nc),
                }
            )
            if created:
                u.set_password('pass1234')
                u.save()
            self.users[uname] = u
            nc += 1

        self.stdout.write(f'  ✓ ۹ سرشیفت ایجاد شد')

        # اپراتورها (۱۲ نفر)
        nc = 1234568000
        for uname, fn, ln, dept in OPERATORS:
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': fn, 'last_name': ln,
                    'role': 'operator', 'department': dept,
                    'national_code': str(nc),
                }
            )
            if created:
                u.set_password('pass1234')
                u.save()
            self.users[uname] = u
            nc += 1

        self.stdout.write(f'  ✓ ۱۲ اپراتور ایجاد شد')
        self.stdout.write(f'  📊 مجموع کاربران: {User.objects.count()}')

    # ═══════════════════════════════════════════════════════
    # ۲. خطوط تولید + شیفت‌ها
    # ═══════════════════════════════════════════════════════

    def _create_lines_and_shifts(self):
        for cfg in LINES_CONFIG:
            line, _ = ProductionLine.objects.get_or_create(
                code=cfg['code'],
                defaults={
                    'name': cfg['name'],
                    'product_type': cfg['product_type'],
                    'target_capacity_kg': cfg['capacity'],
                    'status': 'active',
                    'line_manager': self.users['manager01'],
                    'specs': {
                        'yarn_count': cfg['product_type'],
                        'max_speed': random.randint(800, 1500),
                    },
                }
            )
            self.lines.append(line)

            # شیفت‌های اختصاصی هر خط
            shift_defs = [
                (f'{cfg["code"][-2:]}-A', f'صبح {cfg["name"][:5]}', '06:00', '14:00'),
                (f'{cfg["code"][-2:]}-B', f'عصر {cfg["name"][:5]}', '14:00', '22:00'),
                (f'{cfg["code"][-2:]}-C', f'شب {cfg["name"][:5]}', '22:00', '06:00'),
            ]
            line_shifts = {}
            for scode, sname, st, et in shift_defs:
                s, _ = Shift.objects.get_or_create(
                    code=scode,
                    defaults={
                        'name': sname,
                        'start_time': st,
                        'end_time': et,
                        'production_line': line,
                    }
                )
                line_shifts[scode[-1]] = s  # 'A', 'B', 'C'
            self.shifts[cfg['code']] = line_shifts

        self.stdout.write(f'  ✓ {len(self.lines)} خط تولید ایجاد شد')
        self.stdout.write(f'  ✓ {Shift.objects.count()} شیفت ایجاد شد')

    # ═══════════════════════════════════════════════════════
    # ۳. ماشین‌آلات
    # ═══════════════════════════════════════════════════════

    def _create_machines(self):
        total = 0
        manufacturers = ['Rieter', 'Trützschler', 'LMW', 'Toyota', 'Saurer']
        for i, cfg in enumerate(LINES_CONFIG):
            line = self.lines[i]
            line_machines = {}
            for mtype, items in cfg['machines'].items():
                type_machines = []
                for code, name in items:
                    m, _ = Machine.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'machine_type': mtype,
                            'production_line': line,
                            'status': 'active',
                            'manufacturer': random.choice(manufacturers),
                            'model_name': f'Model-{random.randint(100,999)}',
                            'year_installed': random.randint(2018, 2024),
                            'location': f'سالن {line.code}',
                            'specs': {
                                'max_speed': random.randint(500, 2000),
                                'power_kw': random.randint(5, 75),
                            },
                        }
                    )
                    type_machines.append(m)
                    total += 1
                line_machines[mtype] = type_machines
            self.machines[cfg['code']] = line_machines

        # یک ماشین تعمیری بذاریم
        if self.machines.get('LINE-02', {}).get('carding'):
            m = self.machines['LINE-02']['carding'][-1]
            m.status = 'maintenance'
            m.save()

        self.stdout.write(f'  ✓ {total} ماشین ایجاد شد (۱ در حال تعمیر)')

    # ═══════════════════════════════════════════════════════
    # ۴. اختصاص سرشیفت‌ها
    # ═══════════════════════════════════════════════════════

    def _create_shift_assignments(self):
        shift_codes = ['A', 'B', 'C']
        cnt = 0
        for si, (uname, fn, ln, li) in enumerate(SUPERVISORS):
            line = self.lines[li]
            shift_code = shift_codes[si % 3]
            line_shifts = self.shifts[line.code]
            shift = line_shifts.get(shift_code)
            if shift:
                LineShiftAssignment.objects.get_or_create(
                    production_line=line,
                    shift=shift,
                    defaults={
                        'supervisor': self.users[uname],
                        'is_active': True,
                    }
                )
                cnt += 1
        self.stdout.write(f'  ✓ {cnt} اختصاص سرشیفت ایجاد شد (۳ خط × ۳ شیفت)')

    # ═══════════════════════════════════════════════════════
    # ۵. انبار الیاف
    # ═══════════════════════════════════════════════════════

    def _create_fiber_inventory(self):
        # دسته‌بندی‌ها
        cats = {}
        for code, name, desc in FIBER_CATEGORIES:
            c, _ = FiberCategory.objects.get_or_create(
                code=code, defaults={'name': name, 'description': desc}
            )
            cats[code] = c

        # موجودی: ۲۰ بسته الیاف
        fibers_data = [
            ('PES', 'FIB-14041015-001', 500, 420, 'A', 'سفید', 1.5, 38, 'ردیف ۱ - قفسه الف'),
            ('PES', 'FIB-14041015-002', 500, 350, 'A', 'سفید', 1.5, 38, 'ردیف ۱ - قفسه ب'),
            ('PES', 'FIB-14041020-003', 600, 600, 'A', 'سفید', 1.2, 44, 'ردیف ۲ - قفسه الف'),
            ('PES', 'FIB-14041020-004', 600, 500, 'B', 'سفید', 1.2, 44, 'ردیف ۲ - قفسه ب'),
            ('VIS', 'FIB-14041010-005', 400, 280, 'A', 'اکرو', 1.3, 40, 'ردیف ۳ - قفسه الف'),
            ('VIS', 'FIB-14041010-006', 400, 400, 'A', 'اکرو', 1.3, 40, 'ردیف ۳ - قفسه ب'),
            ('VIS', 'FIB-14041025-007', 300, 300, 'B', 'اکرو', 1.5, 38, 'ردیف ۳ - قفسه ج'),
            ('COT', 'FIB-14040915-008', 350, 150, 'A', 'سفید طبیعی', 1.8, 28, 'ردیف ۴ - قفسه الف'),
            ('COT', 'FIB-14041001-009', 350, 350, 'A', 'سفید طبیعی', 1.8, 28, 'ردیف ۴ - قفسه ب'),
            ('COT', 'FIB-14041005-010', 400, 300, 'A', 'سفید طبیعی', 1.6, 32, 'ردیف ۴ - قفسه ج'),
            ('ACR', 'FIB-14041101-011', 250, 250, 'A', 'سفید', 2.0, 60, 'ردیف ۵ - قفسه الف'),
            ('ACR', 'FIB-14041101-012', 250, 200, 'B', 'سفید', 2.0, 60, 'ردیف ۵ - قفسه ب'),
            ('WOL', 'FIB-14040820-013', 150, 50, 'A', 'طبیعی', 3.5, 75, 'ردیف ۶ - قفسه الف'),
            ('WOL', 'FIB-14041015-014', 150, 150, 'A', 'طبیعی', 3.5, 75, 'ردیف ۶ - قفسه ب'),
            ('PES', 'FIB-14041101-015', 700, 700, 'A', 'سفید', 1.5, 38, 'ردیف ۱ - قفسه ج'),
            ('PES', 'FIB-14041105-016', 500, 500, 'A', 'سفید', 1.2, 44, 'ردیف ۱ - قفسه د'),
            ('VIS', 'FIB-14041105-017', 450, 450, 'A', 'اکرو', 1.3, 40, 'ردیف ۳ - قفسه د'),
            ('COT', 'FIB-14041110-018', 300, 300, 'A', 'سفید طبیعی', 1.8, 28, 'ردیف ۴ - قفسه د'),
            ('PES', 'FIB-14041112-019', 400, 400, 'A', 'رنگی-آبی', 1.5, 38, 'ردیف ۷ - قفسه الف'),
            ('VIS', 'FIB-14041112-020', 300, 300, 'A', 'رنگی-قرمز', 1.3, 40, 'ردیف ۷ - قفسه ب'),
        ]

        for cat_code, batch, init_w, cur_w, grade, color, denier, staple, loc in fibers_data:
            f, _ = FiberStock.objects.get_or_create(
                batch_number=batch,
                defaults={
                    'category': cats[cat_code],
                    'supplier': random.choice(['شرکت الیاف ایران', 'پارس‌الیاف', 'صنایع پتروشیمی', 'نساجی شمال']),
                    'color_raw': color,
                    'denier': denier,
                    'staple_length': staple,
                    'initial_weight': init_w,
                    'current_weight': cur_w,
                    'unit_price': random.randint(800000, 2500000),
                    'received_date': TODAY - timedelta(days=random.randint(5, 60)),
                    'warehouse_loc': loc,
                    'status': 'consumed' if cur_w == 0 else ('available' if cur_w > 50 else 'reserved'),
                    'quality_grade': grade,
                }
            )
            self.fibers.append(f)

        self.stdout.write(f'  ✓ {FiberCategory.objects.count()} دسته الیاف + {len(self.fibers)} بسته موجودی')

    # ═══════════════════════════════════════════════════════
    # ۶. رنگ + شیمیایی
    # ═══════════════════════════════════════════════════════

    def _create_dye_chemical_inventory(self):
        dyes_data = [
            ('DY-R-001', 'قرمز راکتیو ۳BS', 'reactive', 'قرمز', 25, 18, 'kg'),
            ('DY-R-002', 'آبی راکتیو MR', 'reactive', 'آبی', 30, 25, 'kg'),
            ('DY-R-003', 'زرد راکتیو RGB', 'reactive', 'زرد', 20, 20, 'kg'),
            ('DY-D-001', 'آبی دیسپرس SE', 'disperse', 'آبی', 15, 12, 'kg'),
            ('DY-D-002', 'قرمز دیسپرس FF', 'disperse', 'قرمز', 15, 10, 'kg'),
            ('DY-A-001', 'مشکی اسیدی ML', 'acid', 'مشکی', 20, 15, 'kg'),
            ('DY-V-001', 'سبز خمی GBN', 'vat', 'سبز', 10, 8, 'kg'),
            ('DY-M-001', 'نارنجی مستقیم', 'direct', 'نارنجی', 12, 12, 'kg'),
        ]
        for code, name, dtype, family, init_w, cur_w, unit in dyes_data:
            d, _ = DyeStock.objects.get_or_create(
                code=code,
                defaults={
                    'name': name, 'dye_type': dtype, 'color_family': family,
                    'manufacturer': random.choice(['Huntsman', 'DyStar', 'Archroma']),
                    'batch_number': f'LOT-{random.randint(10000,99999)}',
                    'initial_weight': init_w, 'current_weight': cur_w, 'unit': unit,
                    'unit_price': random.randint(5000000, 15000000),
                    'received_date': TODAY - timedelta(days=random.randint(10, 45)),
                    'storage_temp': 25,
                    'status': 'available',
                }
            )
            self.dyes.append(d)

        chems_data = [
            ('CH-AC-01', 'اسید استیک', 'acid', 80, 60, 'liter', 99.5),
            ('CH-AL-01', 'سود کاستیک', 'alkali', 50, 35, 'kg', 48.0),
            ('CH-SA-01', 'نمک صنعتی', 'salt', 200, 150, 'kg', None),
            ('CH-SF-01', 'نرم‌کننده سیلیکونی', 'softener', 30, 25, 'liter', None),
            ('CH-FX-01', 'تثبیت‌کننده DF', 'fixative', 15, 12, 'kg', None),
            ('CH-AX-01', 'دیسپرس‌کننده', 'auxiliary', 20, 18, 'liter', None),
            ('CH-AC-02', 'اسید سولفوریک', 'acid', 40, 30, 'liter', 98.0),
            ('CH-AL-02', 'کربنات سدیم', 'alkali', 100, 80, 'kg', None),
        ]
        for code, name, ctype, init_a, cur_a, unit, conc in chems_data:
            c, _ = ChemicalStock.objects.get_or_create(
                code=code,
                defaults={
                    'name': name, 'chemical_type': ctype,
                    'manufacturer': random.choice(['مرک', 'BASF', 'شیمیایی ایران']),
                    'batch_number': f'CB-{random.randint(10000,99999)}',
                    'initial_amount': init_a, 'current_amount': cur_a, 'unit': unit,
                    'concentration': conc,
                    'unit_price': random.randint(500000, 5000000),
                    'received_date': TODAY - timedelta(days=random.randint(10, 60)),
                    'status': 'available',
                }
            )
            self.chemicals.append(c)

        self.stdout.write(f'  ✓ {len(self.dyes)} رنگ + {len(self.chemicals)} ماده شیمیایی')

    # ═══════════════════════════════════════════════════════
    # ۷. مشتریان + شیدها
    # ═══════════════════════════════════════════════════════

    def _create_customers_and_shades(self):
        for name, company, city, province, phone in CUSTOMERS:
            c, _ = Customer.objects.get_or_create(
                name=name,
                defaults={
                    'company': company, 'city': city, 'province': province,
                    'phone': phone, 'credit_limit': random.randint(50, 500) * 10000000,
                    'is_active': True,
                }
            )
            self.customers_obj.append(c)

        shades_data = [
            ('SH-1001', 'قرمز آتشی', '#E53935'),
            ('SH-1002', 'آبی آسمانی', '#42A5F5'),
            ('SH-1003', 'سبز زمردی', '#66BB6A'),
            ('SH-1004', 'زرد طلایی', '#FDD835'),
            ('SH-1005', 'مشکی کلاسیک', '#212121'),
            ('SH-1006', 'سفید شیری', '#FAFAFA'),
            ('SH-1007', 'نارنجی پاییزی', '#FF7043'),
            ('SH-1008', 'بنفش سلطنتی', '#AB47BC'),
        ]
        for code, name, hex_c in shades_data:
            s, _ = ColorShade.objects.get_or_create(
                code=code,
                defaults={
                    'name': name, 'color_hex': hex_c,
                    'recipe': {'dye_pct': round(random.uniform(1, 5), 2), 'temp': random.randint(80, 130)},
                    'is_approved': True,
                    'approved_by': self.users['manager01'],
                    'approved_at': NOW - timedelta(days=random.randint(1, 30)),
                }
            )
            self.shades.append(s)

        self.stdout.write(f'  ✓ {len(self.customers_obj)} مشتری + {len(self.shades)} شید رنگی')

    # ═══════════════════════════════════════════════════════
    # ۸. سفارشات
    # ═══════════════════════════════════════════════════════

    def _create_orders(self):
        statuses = ['draft', 'confirmed', 'in_production', 'in_production',
                     'quality_check', 'ready', 'delivered', 'delivered']
        yarn_types = ['نخ پنبه‌ای', 'نخ پلی‌استر', 'نخ مخلوط PES/VIS']
        yarn_counts = ['Ne 20/1', 'Ne 24/1', 'Ne 30/1', 'Ne 36/1']

        for idx in range(15):
            onum = f'ORD-{(TODAY - timedelta(days=60-idx*4)).strftime("%Y%m%d")}-{idx+1:03d}'
            cust = random.choice(self.customers_obj)
            shade = random.choice(self.shades)
            line = self.lines[idx % 3]
            st = statuses[idx % len(statuses)]
            qty = Decimal(str(random.randint(500, 5000)))

            o, _ = Order.objects.get_or_create(
                order_number=onum,
                defaults={
                    'customer': cust,
                    'production_line': line,
                    'color_shade': shade,
                    'yarn_type': random.choice(yarn_types),
                    'yarn_count': random.choice(yarn_counts),
                    'quantity_kg': qty,
                    'unit_price': random.randint(800000, 2000000),
                    'total_price': qty * random.randint(800000, 2000000),
                    'delivery_date': TODAY + timedelta(days=random.randint(-10, 30)),
                    'priority': random.choice(['low', 'normal', 'normal', 'high', 'urgent']),
                    'status': st,
                    'progress_pct': {'draft': 0, 'confirmed': 5, 'in_production': random.randint(20, 80),
                                     'quality_check': 90, 'ready': 100, 'delivered': 100}.get(st, 0),
                    'created_by': self.users['manager01'],
                }
            )
            self.orders_obj.append(o)

        self.stdout.write(f'  ✓ {len(self.orders_obj)} سفارش ایجاد شد')

    # ═══════════════════════════════════════════════════════
    # ۹. حلاجی
    # ═══════════════════════════════════════════════════════

    def _create_blowroom_batches(self):
        self.bl_batches = {}  # {line_code: [Batch]}
        ops = [self.users[f'op_{i:02d}'] for i in range(1, 7)]
        batch_num = 1

        for li, line in enumerate(self.lines):
            line_batches = []
            line_code = line.code
            machines = self.machines[line_code].get('blowroom', [])
            if not machines:
                continue
            machine = machines[0]
            shifts = list(self.shifts[line_code].values())

            # ۵ بچ برای هر خط (۳ روز اخیر)
            for d in range(3):
                prod_date = TODAY - timedelta(days=d)
                for s_idx in range(2 if d > 0 else 1):
                    bn = f'BL-{prod_date.strftime("%Y%m%d")}-{batch_num:03d}'
                    inp_w = Decimal(str(random.randint(300, 600)))
                    out_w = inp_w * Decimal('0.95')
                    waste = inp_w - out_w

                    status = 'completed' if d > 0 else 'in_progress'

                    b, _ = BlowroomBatch.objects.get_or_create(
                        batch_number=bn,
                        defaults={
                            'production_line': line,
                            'machine': machine,
                            'operator': random.choice(ops),
                            'shift': shifts[s_idx % len(shifts)],
                            'order': self.orders_obj[li] if li < len(self.orders_obj) else None,
                            'production_date': prod_date,
                            'status': status,
                            'started_at': datetime.combine(prod_date, time(6 + s_idx * 8, 0)),
                            'completed_at': datetime.combine(
                                prod_date, time(12 + s_idx * 8, 0)
                            ) if status == 'completed' else None,
                            'total_input_weight': inp_w,
                            'output_weight': out_w,
                            'waste_weight': waste,
                            'waste_pct': round(float(waste / inp_w * 100), 2),
                            'blend_recipe': {'PES': 70, 'VIS': 30} if li == 2 else (
                                {'COT': 100} if li == 0 else {'PES': 100}
                            ),
                            'metadata': {'humidity': round(random.uniform(55, 70), 1)},
                        }
                    )
                    # ورودی‌ها
                    available_fibers = [f for f in self.fibers if f.current_weight > 50]
                    if available_fibers:
                        fib = random.choice(available_fibers)
                        BatchInput.objects.get_or_create(
                            batch=b, fiber_stock=fib,
                            defaults={'weight_used': inp_w, 'percentage': 100}
                        )
                    line_batches.append(b)
                    batch_num += 1

            self.bl_batches[line_code] = line_batches

        total = BlowroomBatch.objects.count()
        self.stdout.write(f'  ✓ {total} بچ حلاجی')

    # ═══════════════════════════════════════════════════════
    # ۱۰. کاردینگ
    # ═══════════════════════════════════════════════════════

    def _create_carding_productions(self):
        self.cd_batches = {}
        ops = [self.users[f'op_{i:02d}'] for i in range(1, 7)]
        batch_num = 1

        for li, line in enumerate(self.lines):
            line_code = line.code
            machines = self.machines[line_code].get('carding', [])
            shifts = list(self.shifts[line_code].values())
            bl_list = self.bl_batches.get(line_code, [])
            cd_list = []

            for bi, bl in enumerate(bl_list):
                machine = machines[bi % len(machines)] if machines else None
                if not machine:
                    continue
                bn = f'CR-{bl.production_date.strftime("%Y%m%d")}-{batch_num:03d}'

                c, _ = CardingProduction.objects.get_or_create(
                    batch_number=bn,
                    defaults={
                        'production_line': line,
                        'machine': machine,
                        'operator': random.choice(ops),
                        'shift': shifts[bi % len(shifts)],
                        'order': bl.order,
                        'production_date': bl.production_date,
                        'status': bl.status,
                        'started_at': bl.started_at,
                        'completed_at': bl.completed_at,
                        'blowroom_batch': bl,
                        'speed_rpm': Decimal(str(random.randint(80, 120))),
                        'sliver_count': Decimal('4.500'),
                        'sliver_weight_gperm': Decimal('4.200'),
                        'input_weight': bl.output_weight,
                        'output_weight': bl.output_weight * Decimal('0.97') if bl.output_weight else None,
                        'waste_weight': bl.output_weight * Decimal('0.03') if bl.output_weight else None,
                        'waste_pct': Decimal('3.0'),
                        'neps_count': random.randint(10, 80),
                        'metadata': {'nep_trend': 'stable'},
                    }
                )
                cd_list.append(c)
                batch_num += 1

            self.cd_batches[line_code] = cd_list

        self.stdout.write(f'  ✓ {CardingProduction.objects.count()} بچ کاردینگ')

    # ═══════════════════════════════════════════════════════
    # ۱۱. پاساژ
    # ═══════════════════════════════════════════════════════

    def _create_passage_productions(self):
        self.ps_batches = {}
        ops = [self.users[f'op_{i:02d}'] for i in range(1, 7)]
        batch_num = 1

        for li, line in enumerate(self.lines):
            line_code = line.code
            machines = self.machines[line_code].get('passage', [])
            shifts = list(self.shifts[line_code].values())
            cd_list = self.cd_batches.get(line_code, [])
            ps_list = []

            for ci, cd in enumerate(cd_list):
                machine = machines[ci % len(machines)] if machines else None
                if not machine:
                    continue
                bn = f'PS-{cd.production_date.strftime("%Y%m%d")}-{batch_num:03d}'

                p, created = PassageProduction.objects.get_or_create(
                    batch_number=bn,
                    defaults={
                        'production_line': line,
                        'machine': machine,
                        'operator': random.choice(ops),
                        'shift': shifts[ci % len(shifts)],
                        'order': cd.order,
                        'production_date': cd.production_date,
                        'status': cd.status,
                        'started_at': cd.started_at,
                        'completed_at': cd.completed_at,
                        'passage_number': 1,
                        'num_inputs': 6,
                        'draft_ratio': Decimal('6.500'),
                        'output_sliver_count': Decimal('4.200'),
                        'output_weight_gperm': Decimal('4.000'),
                        'input_total_weight': cd.output_weight,
                        'output_weight': cd.output_weight * Decimal('0.99') if cd.output_weight else None,
                        'speed_mpm': Decimal(str(random.randint(200, 400))),
                        'evenness_cv': Decimal(str(round(random.uniform(2.5, 5.0), 2))),
                        'metadata': {'cv_trend': 'improving'},
                    }
                )
                if created:
                    PassageInput.objects.get_or_create(
                        passage_production=p, input_position=1,
                        defaults={
                            'source_type': 'carding',
                            'source_id': cd.id,
                            'source_batch_number': cd.batch_number,
                            'weight_used': cd.output_weight,
                        }
                    )
                ps_list.append(p)
                batch_num += 1

            self.ps_batches[line_code] = ps_list

        self.stdout.write(f'  ✓ {PassageProduction.objects.count()} بچ پاساژ')

    # ═══════════════════════════════════════════════════════
    # ۱۲. فینیشر
    # ═══════════════════════════════════════════════════════

    def _create_finisher_productions(self):
        self.fn_batches = {}
        ops = [self.users[f'op_{i:02d}'] for i in range(1, 7)]
        batch_num = 1

        for li, line in enumerate(self.lines):
            line_code = line.code
            machines = self.machines[line_code].get('finisher', [])
            shifts = list(self.shifts[line_code].values())
            ps_list = self.ps_batches.get(line_code, [])
            fn_list = []

            for pi, ps in enumerate(ps_list):
                machine = machines[0] if machines else None
                if not machine:
                    continue
                bn = f'FN-{ps.production_date.strftime("%Y%m%d")}-{batch_num:03d}'

                f, _ = FinisherProduction.objects.get_or_create(
                    batch_number=bn,
                    defaults={
                        'production_line': line,
                        'machine': machine,
                        'operator': random.choice(ops),
                        'shift': shifts[pi % len(shifts)],
                        'order': ps.order,
                        'production_date': ps.production_date,
                        'status': ps.status,
                        'started_at': ps.started_at,
                        'completed_at': ps.completed_at,
                        'passage_production': ps,
                        'draft_ratio': Decimal('8.000'),
                        'twist_tpm': Decimal(str(random.randint(30, 60))),
                        'output_sliver_count': Decimal('0.800'),
                        'speed_mpm': Decimal(str(random.randint(150, 300))),
                        'input_weight': ps.output_weight,
                        'output_weight': ps.output_weight * Decimal('0.99') if ps.output_weight else None,
                        'metadata': {},
                    }
                )
                fn_list.append(f)
                batch_num += 1

            self.fn_batches[line_code] = fn_list

        self.stdout.write(f'  ✓ {FinisherProduction.objects.count()} بچ فینیشر')

    # ═══════════════════════════════════════════════════════
    # ۱۳. رینگ
    # ═══════════════════════════════════════════════════════

    def _create_spinning_productions(self):
        self.sp_batches = {}
        ops = [self.users[f'op_{i:02d}'] for i in range(1, 7)]
        batch_num = 1

        for li, line in enumerate(self.lines):
            line_code = line.code
            machines = self.machines[line_code].get('ring', [])
            shifts = list(self.shifts[line_code].values())
            fn_list = self.fn_batches.get(line_code, [])
            sp_list = []

            for fi, fn in enumerate(fn_list):
                machine = machines[fi % len(machines)] if machines else None
                if not machine:
                    continue
                bn = f'SP-{fn.production_date.strftime("%Y%m%d")}-{batch_num:03d}'

                s, _ = SpinningProduction.objects.get_or_create(
                    batch_number=bn,
                    defaults={
                        'production_line': line,
                        'machine': machine,
                        'operator': random.choice(ops),
                        'shift': shifts[fi % len(shifts)],
                        'order': fn.order,
                        'production_date': fn.production_date,
                        'status': fn.status,
                        'started_at': fn.started_at,
                        'completed_at': fn.completed_at,
                        'finisher_production': fn,
                        'spindle_speed_rpm': random.randint(10000, 18000),
                        'twist_tpm': Decimal(str(random.randint(600, 1000))),
                        'twist_direction': random.choice(['S', 'Z']),
                        'yarn_count': Decimal(str([30, 20, 24][li])),
                        'traveler_number': f'T-{random.randint(1,5)}/0',
                        'traveler_type': 'C1 EL',
                        'ring_diameter': Decimal('42.00'),
                        'input_weight': fn.output_weight,
                        'output_weight': fn.output_weight * Decimal('0.96') if fn.output_weight else None,
                        'num_spindles_active': random.randint(400, 480),
                        'num_spindles_total': 480,
                        'breakage_count': random.randint(2, 25),
                        'efficiency_pct': Decimal(str(round(random.uniform(85, 97), 2))),
                        'metadata': {
                            'avg_breakage_per_1000h': round(random.uniform(10, 50), 1),
                        },
                    }
                )
                sp_list.append(s)
                batch_num += 1

            self.sp_batches[line_code] = sp_list

        self.stdout.write(f'  ✓ {SpinningProduction.objects.count()} بچ رینگ')

    # ═══════════════════════════════════════════════════════
    # ۱۴. رنگرزی
    # ═══════════════════════════════════════════════════════

    def _create_dyeing_batches(self):
        ops = [self.users['op_07'], self.users['op_08']]
        batch_num = 1

        for li, line in enumerate(self.lines):
            line_code = line.code
            machines = self.machines[line_code].get('dyeing', [])
            shifts = list(self.shifts[line_code].values())
            if not machines:
                continue
            machine = machines[0]

            for d in range(3):
                prod_date = TODAY - timedelta(days=d)
                bn = f'DY-{prod_date.strftime("%Y%m%d")}-{batch_num:03d}'
                shade = self.shades[batch_num % len(self.shades)]
                fiber_w = Decimal(str(random.randint(100, 300)))
                status_choices = ['completed', 'completed', 'in_progress', 'drying', 'cooling']
                st = 'in_progress' if d == 0 else 'completed'

                db, created = DyeingBatch.objects.get_or_create(
                    batch_number=bn,
                    defaults={
                        'order': self.orders_obj[li] if li < len(self.orders_obj) else None,
                        'color_shade': shade,
                        'machine': machine,
                        'operator': random.choice(ops),
                        'shift': shifts[d % len(shifts)],
                        'production_date': prod_date,
                        'fiber_weight': fiber_w,
                        'liquor_ratio': Decimal('8.00'),
                        'temperature': Decimal(str(random.randint(80, 130))),
                        'duration_min': random.randint(60, 180),
                        'ph_value': Decimal(str(round(random.uniform(4.5, 9.0), 2))),
                        'status': st,
                        'started_at': datetime.combine(prod_date, time(7, 0)),
                        'completed_at': datetime.combine(
                            prod_date, time(15, 0)
                        ) if st == 'completed' else None,
                        'quality_result': 'pass' if st == 'completed' else '',
                        'metadata': {'dye_exhaustion_pct': round(random.uniform(85, 98), 1)},
                    }
                )
                # مصرف مواد
                if created and self.dyes:
                    dye = random.choice(self.dyes)
                    ChemicalUsage.objects.create(
                        dyeing_batch=db, material_type='dye', dye_stock=dye,
                        quantity_used=Decimal(str(round(random.uniform(0.5, 3.0), 3))),
                        unit='kg', step_name='رنگرزی', sequence_order=1,
                    )
                if created and self.chemicals:
                    chem = random.choice(self.chemicals)
                    ChemicalUsage.objects.create(
                        dyeing_batch=db, material_type='chemical', chemical_stock=chem,
                        quantity_used=Decimal(str(round(random.uniform(1.0, 5.0), 3))),
                        unit='kg', step_name='شست‌وشو', sequence_order=2,
                    )
                batch_num += 1

        self.stdout.write(f'  ✓ {DyeingBatch.objects.count()} بچ رنگرزی + {ChemicalUsage.objects.count()} مصرف مواد')

    # ═══════════════════════════════════════════════════════
    # ۱۵. دیگ بخار + خشک‌کن
    # ═══════════════════════════════════════════════════════

    def _create_boiler_dryer_logs(self):
        ops = [self.users['op_07'], self.users['op_08']]

        for li, line in enumerate(self.lines):
            line_code = line.code
            boilers = self.machines[line_code].get('boiler', [])
            dryers = self.machines[line_code].get('dryer', [])
            shifts = list(self.shifts[line_code].values())

            for d in range(5):
                log_date = TODAY - timedelta(days=d)
                if boilers:
                    BoilerLog.objects.get_or_create(
                        machine=boilers[0], log_date=log_date, shift=shifts[0],
                        defaults={
                            'operator': random.choice(ops),
                            'pressure_bar': Decimal(str(round(random.uniform(6.0, 10.0), 2))),
                            'temperature_c': Decimal(str(random.randint(150, 180))),
                            'water_level': Decimal(str(random.randint(60, 90))),
                            'fuel_consumed': Decimal(str(random.randint(100, 300))),
                            'running_hours': Decimal('8.00'),
                            'status': 'running',
                            'metadata': {'efficiency': round(random.uniform(80, 95), 1)},
                        }
                    )
                if dryers:
                    DryerLog.objects.get_or_create(
                        machine=dryers[0], log_date=log_date, shift=shifts[0],
                        defaults={
                            'operator': random.choice(ops),
                            'temperature_c': Decimal(str(random.randint(80, 120))),
                            'duration_min': random.randint(30, 90),
                            'humidity_pct': Decimal(str(round(random.uniform(5, 15), 2))),
                            'status': 'running',
                            'metadata': {},
                        }
                    )

        self.stdout.write(f'  ✓ {BoilerLog.objects.count()} لاگ بخار + {DryerLog.objects.count()} لاگ خشک‌کن')

    # ═══════════════════════════════════════════════════════
    # ۱۶. نگهداری (PM)
    # ═══════════════════════════════════════════════════════

    def _create_maintenance_schedules(self):
        tech = self.users.get('op_09') or self.users.get('op_10')
        cnt = 0
        for line_code, line_machines in self.machines.items():
            for mtype, machines_list in line_machines.items():
                for machine in machines_list:
                    # PM هفتگی
                    Schedule.objects.get_or_create(
                        machine=machine, title=f'سرویس هفتگی {machine.code}',
                        defaults={
                            'maintenance_type': 'preventive',
                            'description': f'بازدید و روغن‌کاری هفتگی {machine.name}',
                            'frequency': 'weekly',
                            'last_done_at': NOW - timedelta(days=random.randint(1, 7)),
                            'next_due_at': NOW + timedelta(days=random.randint(0, 7)),
                            'assigned_to': tech,
                            'priority': 'medium',
                            'is_active': True,
                        }
                    )
                    cnt += 1
                    # PM ماهانه
                    Schedule.objects.get_or_create(
                        machine=machine, title=f'سرویس ماهانه {machine.code}',
                        defaults={
                            'maintenance_type': 'preventive',
                            'description': f'تعویض فیلتر و بازرسی کامل {machine.name}',
                            'frequency': 'monthly',
                            'last_done_at': NOW - timedelta(days=random.randint(15, 30)),
                            'next_due_at': NOW + timedelta(days=random.randint(-5, 25)),
                            'assigned_to': tech,
                            'priority': 'high',
                            'is_active': True,
                        }
                    )
                    cnt += 1

        self.stdout.write(f'  ✓ {cnt} برنامه سرویس (PM)')

    # ═══════════════════════════════════════════════════════
    # ۱۷. دستورهای کار
    # ═══════════════════════════════════════════════════════

    def _create_work_orders(self):
        tech = self.users.get('op_09')
        reporter = self.users.get('op_10') or self.users.get('manager01')
        wo_num = 1

        all_machines = []
        for lm in self.machines.values():
            for ml in lm.values():
                all_machines.extend(ml)

        wo_data = [
            ('تعویض تسمه', 'preventive', 'completed', 'medium', 120),
            ('تعمیر موتور', 'corrective', 'completed', 'high', 240),
            ('بازرسی برق', 'preventive', 'completed', 'low', 60),
            ('تعویض بلبرینگ', 'corrective', 'in_progress', 'critical', 180),
            ('سرویس هیدرولیک', 'preventive', 'open', 'medium', None),
            ('تعمیر سنسور دما', 'emergency', 'open', 'high', None),
            ('تنظیم کشش', 'corrective', 'completed', 'medium', 90),
            ('تعویض روغن گیربکس', 'preventive', 'waiting_parts', 'medium', None),
        ]

        for title, wtype, status, priority, dt_min in wo_data:
            machine = random.choice(all_machines)
            wo_code = f'WO-{TODAY.strftime("%Y%m%d")}-{wo_num:03d}'
            WorkOrder.objects.get_or_create(
                wo_number=wo_code,
                defaults={
                    'machine': machine,
                    'title': f'{title} - {machine.code}',
                    'description': f'{title} برای ماشین {machine.name}',
                    'wo_type': wtype,
                    'priority': priority,
                    'reported_by': reporter,
                    'assigned_to': tech,
                    'status': status,
                    'started_at': NOW - timedelta(hours=random.randint(1, 48)) if status != 'open' else None,
                    'completed_at': NOW - timedelta(hours=random.randint(0, 24)) if status == 'completed' else None,
                    'downtime_min': dt_min,
                    'cost_parts': random.randint(0, 50) * 1000000 if status == 'completed' else 0,
                    'cost_labor': random.randint(5, 20) * 1000000 if status == 'completed' else 0,
                }
            )
            wo_num += 1

        self.stdout.write(f'  ✓ {WorkOrder.objects.count()} دستور کار')

    # ═══════════════════════════════════════════════════════
    # ۱۸. لاگ توقفات
    # ═══════════════════════════════════════════════════════

    def _create_downtime_logs(self):
        ops = [self.users[f'op_{i:02d}'] for i in range(1, 7)]

        all_machines = []
        all_shifts = []
        for line in self.lines:
            for ml in self.machines[line.code].values():
                all_machines.extend(ml)
            all_shifts.extend(self.shifts[line.code].values())

        reasons = [
            ('mechanical', 'شکستگی تسمه', 45, 15),
            ('electrical', 'قطعی برق', 30, 10),
            ('material', 'تمام شدن مواد اولیه', 20, 5),
            ('operator', 'تعویض شیفت', 15, 0),
            ('quality', 'مشکل کیفی - توقف خط', 60, 25),
            ('mechanical', 'گرم شدن بلبرینگ', 90, 35),
            ('planned', 'تعمیرات برنامه‌ریزی شده', 120, 0),
            ('electrical', 'خرابی سنسور', 40, 12),
            ('material', 'تغییر نوع الیاف', 25, 0),
            ('quality', 'نمونه‌برداری کیفیت', 10, 2),
        ]

        for cat, detail, dur, loss in reasons:
            machine = random.choice(all_machines)
            shift = random.choice(all_shifts)
            start = NOW - timedelta(hours=random.randint(2, 72))
            line = None
            for l in self.lines:
                if machine.production_line_id == l.id:
                    line = l
                    break

            DowntimeLog.objects.create(
                production_line=line,
                machine=machine,
                operator=random.choice(ops),
                shift=shift,
                start_time=start,
                end_time=start + timedelta(minutes=dur),
                duration_min=dur,
                reason_category=cat,
                reason_detail=detail,
                production_loss=Decimal(str(loss)) if loss else None,
                metadata={'severity': random.choice(['low', 'medium', 'high'])},
            )

        self.stdout.write(f'  ✓ {DowntimeLog.objects.count()} لاگ توقف')

    # ═══════════════════════════════════════════════════════
    # ۱۹. اعلان‌ها
    # ═══════════════════════════════════════════════════════

    def _create_notifications(self):
        mgr = self.users['manager01']
        notifs = [
            ('PM سررسید شده', 'سرویس هفتگی CR-01 سررسید شده است', 'maintenance', False),
            ('سفارش جدید', 'سفارش ORD-001 ثبت شد', 'info', True),
            ('موجودی کم', 'موجودی پلی‌استر به زیر حد هشدار رسید', 'warning', False),
            ('خرابی ماشین', 'ماشین RG-02 متوقف شده - نیاز به تعمیر', 'danger', False),
            ('تولید تکمیل', 'بچ SP-001 با موفقیت تکمیل شد', 'success', True),
            ('PM آینده', 'سرویس ماهانه PS-01 در ۳ روز آینده', 'maintenance', False),
        ]
        for title, msg, ntype, is_read in notifs:
            Notification.objects.create(
                recipient=mgr, title=title, message=msg,
                notif_type=ntype, is_read=is_read,
            )

        self.stdout.write(f'  ✓ {Notification.objects.count()} اعلان')

    # ═══════════════════════════════════════════════════════
    # خلاصه نهایی
    # ═══════════════════════════════════════════════════════

    def _print_summary(self):
        self.stdout.write(self.style.SUCCESS(
            '\n╔══════════════════════════════════════════════╗\n'
            '║           ✅ داده‌گذاری کامل شد!              ║\n'
            '╚══════════════════════════════════════════════╝'
        ))
        summary = [
            ('کاربران', User.objects.count()),
            ('خطوط تولید', ProductionLine.objects.count()),
            ('شیفت‌ها', Shift.objects.count()),
            ('اختصاص سرشیفت', LineShiftAssignment.objects.count()),
            ('ماشین‌آلات', Machine.objects.count()),
            ('دسته الیاف', FiberCategory.objects.count()),
            ('موجودی الیاف', FiberStock.objects.count()),
            ('موجودی رنگ', DyeStock.objects.count()),
            ('مواد شیمیایی', ChemicalStock.objects.count()),
            ('مشتریان', Customer.objects.count()),
            ('شیدهای رنگی', ColorShade.objects.count()),
            ('سفارشات', Order.objects.count()),
            ('بچ حلاجی', BlowroomBatch.objects.count()),
            ('بچ کاردینگ', CardingProduction.objects.count()),
            ('بچ پاساژ', PassageProduction.objects.count()),
            ('بچ فینیشر', FinisherProduction.objects.count()),
            ('بچ رینگ', SpinningProduction.objects.count()),
            ('بچ رنگرزی', DyeingBatch.objects.count()),
            ('لاگ دیگ بخار', BoilerLog.objects.count()),
            ('لاگ خشک‌کن', DryerLog.objects.count()),
            ('برنامه PM', Schedule.objects.count()),
            ('دستور کار', WorkOrder.objects.count()),
            ('لاگ توقف', DowntimeLog.objects.count()),
            ('اعلان‌ها', Notification.objects.count()),
        ]
        total = 0
        for label, cnt in summary:
            self.stdout.write(f'  {label:.<30s} {cnt}')
            total += cnt
        self.stdout.write(self.style.SUCCESS(f'\n  {"مجموع رکوردها":.<30s} {total}'))
        self.stdout.write(self.style.WARNING(
            '\n  🔑 رمز عبور تمام کاربران: pass1234 (ادمین: admin1234)'
            '\n  🌐 ورود: http://localhost:8000/accounts/login/'
            '\n  📊 داشبورد: http://localhost:8000/dashboard/'
            '\n  📺 مانیتورینگ: http://localhost:8000/dashboard/line-monitor/'
        ))
