"""
Diaco MES - Demo Data Generator
=================================
دستور مدیریتی برای تولید داده‌های دمو.
اجرا: python manage.py generate_demo --settings=config.settings.production
cron: هر ساعت یک‌بار اجرا می‌شود و بچ‌های جدید اضافه می‌کند.
"""
import random
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'تولید داده‌های دموی زنده برای نمایش به مشتریان'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='پاک‌سازی و شروع از صفر',
        )
        parser.add_argument(
            '--hourly',
            action='store_true',
            help='فقط بچ‌های جدید این ساعت (برای cron)',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('پاک‌سازی داده‌های قبلی...')
            self._reset_demo_data()

        if options['hourly']:
            self.stdout.write('تولید داده‌های ساعتی...')
            self._generate_hourly_batches()
        else:
            self.stdout.write('تولید داده‌های پایه دمو...')
            self._generate_base_data()
            self._generate_hourly_batches()

        self.stdout.write(self.style.SUCCESS('داده‌های دمو با موفقیت ایجاد شدند!'))

    # ══════════════════════════════════════════════════════
    # RESET
    # ══════════════════════════════════════════════════════

    def _reset_demo_data(self):
        """پاک‌سازی همه داده‌های دمو"""
        from apps.blowroom.models import Batch as BlBatch
        from apps.blowroom.models import BatchInput
        from apps.carding.models import Production as CrProd
        from apps.passage.models import Production as PsProd
        from apps.finisher.models import Production as FnProd
        from apps.spinning.models import Production as SpProd, TravelerReplacement
        from apps.winding.models import Production as WdProd
        from apps.tfo.models import Production as TfoProd
        from apps.heatset.models import Batch as HsProd
        from apps.maintenance.models import WorkOrder, DowntimeLog, Schedule, MachineServiceDate
        from apps.orders.models import Order, Customer, ColorShade
        from apps.inventory.models import FiberStock, DyeStock, ChemicalStock, StockTransaction, FiberCategory
        from apps.core.models import Machine, ProductionLine, Shift, LineShiftAssignment
        from apps.accounts.models import User

        for model in [
            BatchInput, BlBatch, CrProd, PsProd, FnProd, SpProd,
            TravelerReplacement, WdProd, TfoProd, HsProd,
            DowntimeLog, WorkOrder, MachineServiceDate, Schedule,
            Order, ColorShade, Customer,
            StockTransaction, FiberStock, DyeStock, ChemicalStock, FiberCategory,
            LineShiftAssignment, Shift, Machine, ProductionLine,
        ]:
            model.objects.all().delete()

        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('  پاک‌سازی کامل شد.')

    # ══════════════════════════════════════════════════════
    # BASE DATA
    # ══════════════════════════════════════════════════════

    def _generate_base_data(self):
        """تولید داده‌های پایه که یک‌بار ساخته می‌شوند"""
        self._create_users()
        self._create_production_lines()
        self._create_machines()
        self._create_shifts()
        self._create_inventory()
        self._create_customers()
        self._create_color_shades()
        self._create_orders()
        self._create_maintenance_schedules()

    # ══════════════════════════════════════════════════════
    # USERS
    # ══════════════════════════════════════════════════════

    def _create_users(self):
        from apps.accounts.models import User

        users_data = [
            # مدیران
            {'username': 'manager1', 'first_name': 'رضا', 'last_name': 'احمدی',
             'role': 'manager', 'department': 'production', 'password': 'Demo@1404'},
            # سرپرستان
            {'username': 'supervisor1', 'first_name': 'علی', 'last_name': 'محمدی',
             'role': 'supervisor', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'supervisor2', 'first_name': 'حسن', 'last_name': 'رضایی',
             'role': 'supervisor', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'supervisor3', 'first_name': 'مریم', 'last_name': 'کریمی',
             'role': 'supervisor', 'department': 'production', 'password': 'Demo@1404'},
            # اپراتورها
            {'username': 'op_blow1', 'first_name': 'محمد', 'last_name': 'حسینی',
             'role': 'operator', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'op_card1', 'first_name': 'فاطمه', 'last_name': 'نجفی',
             'role': 'operator', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'op_ring1', 'first_name': 'سعید', 'last_name': 'موسوی',
             'role': 'operator', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'op_wind1', 'first_name': 'زهرا', 'last_name': 'صادقی',
             'role': 'operator', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'op_tfo1', 'first_name': 'امیر', 'last_name': 'غلامی',
             'role': 'operator', 'department': 'production', 'password': 'Demo@1404'},
            {'username': 'op_hs1', 'first_name': 'نرگس', 'last_name': 'عباسی',
             'role': 'operator', 'department': 'production', 'password': 'Demo@1404'},
            # نگهداری
            {'username': 'tech1', 'first_name': 'کریم', 'last_name': 'اکبری',
             'role': 'operator', 'department': 'maintenance', 'password': 'Demo@1404'},
            # انبار
            {'username': 'warehouse1', 'first_name': 'ناصر', 'last_name': 'جعفری',
             'role': 'operator', 'department': 'warehouse', 'password': 'Demo@1404'},
            # ناظر
            {'username': 'viewer1', 'first_name': 'لیلا', 'last_name': 'تهرانی',
             'role': 'viewer', 'department': 'office', 'password': 'Demo@1404'},
        ]

        for data in users_data:
            pwd = data.pop('password')
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(password=pwd, **data)
                self.stdout.write(f'  کاربر: {user.get_full_name()} ({user.get_role_display()})')

    # ══════════════════════════════════════════════════════
    # PRODUCTION LINES
    # ══════════════════════════════════════════════════════

    def _create_production_lines(self):
        from apps.core.models import ProductionLine
        from apps.accounts.models import User

        manager = User.objects.filter(role='manager').first()

        lines = [
            {'code': 'LINE-01', 'name': 'خط یک - نخ فرش ۱۴۰۰ دنیر',
             'product_type': 'نخ فرش پلی‌استر ۱۴۰۰ دنیر', 'target_capacity_kg': 800},
            {'code': 'LINE-02', 'name': 'خط دو - نخ فرش ۱۰۰۰ دنیر',
             'product_type': 'نخ فرش اکریلیک ۱۰۰۰ دنیر', 'target_capacity_kg': 600},
        ]
        for data in lines:
            if not ProductionLine.objects.filter(code=data['code']).exists():
                line = ProductionLine.objects.create(
                    line_manager=manager,
                    **data
                )
                self.stdout.write(f'  خط تولید: {line.name}')

    # ══════════════════════════════════════════════════════
    # MACHINES
    # ══════════════════════════════════════════════════════

    def _create_machines(self):
        from apps.core.models import Machine, ProductionLine

        line1 = ProductionLine.objects.get(code='LINE-01')
        line2 = ProductionLine.objects.get(code='LINE-02')

        machines_data = [
            # خط ۱
            {'code': 'BL-01', 'name': 'حلاجی یک', 'machine_type': 'blowroom',
             'manufacturer': 'Truetzschler', 'model_name': 'TC-19', 'year_installed': 2018,
             'location': 'سالن حلاجی', 'production_line': line1},
            {'code': 'CR-01', 'name': 'کارد یک', 'machine_type': 'carding',
             'manufacturer': 'Truetzschler', 'model_name': 'TC-30i', 'year_installed': 2018,
             'location': 'سالن کاردینگ', 'production_line': line1},
            {'code': 'CR-02', 'name': 'کارد دو', 'machine_type': 'carding',
             'manufacturer': 'Truetzschler', 'model_name': 'TC-30i', 'year_installed': 2019,
             'location': 'سالن کاردینگ', 'production_line': line1},
            {'code': 'PS-01', 'name': 'پاساژ یک', 'machine_type': 'passage',
             'manufacturer': 'Rieter', 'model_name': 'RSB-D 45', 'year_installed': 2018,
             'location': 'سالن پاساژ', 'production_line': line1},
            {'code': 'FN-01', 'name': 'فینیشر یک', 'machine_type': 'finisher',
             'manufacturer': 'Rieter', 'model_name': 'F 40', 'year_installed': 2018,
             'location': 'سالن فینیشر', 'production_line': line1},
            {'code': 'RG-01', 'name': 'رینگ یک', 'machine_type': 'ring',
             'manufacturer': 'Zinser', 'model_name': '72XL', 'year_installed': 2018,
             'location': 'سالن رینگ الف', 'production_line': line1},
            {'code': 'RG-02', 'name': 'رینگ دو', 'machine_type': 'ring',
             'manufacturer': 'Zinser', 'model_name': '72XL', 'year_installed': 2019,
             'location': 'سالن رینگ الف', 'production_line': line1},
            {'code': 'WD-01', 'name': 'بوبین‌پیچ یک', 'machine_type': 'winding',
             'manufacturer': 'Autoconer', 'model_name': 'X6', 'year_installed': 2020,
             'location': 'سالن تکمیل', 'production_line': line1},
            {'code': 'TF-01', 'name': 'دولاتابی یک', 'machine_type': 'tfo',
             'manufacturer': 'Volkmann', 'model_name': 'VTS 08', 'year_installed': 2020,
             'location': 'سالن تکمیل', 'production_line': line1},
            {'code': 'HS-01', 'name': 'هیت‌ست یک', 'machine_type': 'heatset',
             'manufacturer': 'Superba', 'model_name': 'V008', 'year_installed': 2020,
             'location': 'سالن تکمیل', 'production_line': line1},
            # خط ۲
            {'code': 'BL-02', 'name': 'حلاجی دو', 'machine_type': 'blowroom',
             'manufacturer': 'Truetzschler', 'model_name': 'TC-19', 'year_installed': 2021,
             'location': 'سالن حلاجی', 'production_line': line2},
            {'code': 'CR-03', 'name': 'کارد سه', 'machine_type': 'carding',
             'manufacturer': 'Truetzschler', 'model_name': 'TC-30i', 'year_installed': 2021,
             'location': 'سالن کاردینگ', 'production_line': line2},
            {'code': 'RG-03', 'name': 'رینگ سه', 'machine_type': 'ring',
             'manufacturer': 'Zinser', 'model_name': '72XL', 'year_installed': 2021,
             'location': 'سالن رینگ ب', 'production_line': line2},
            {'code': 'WD-02', 'name': 'بوبین‌پیچ دو', 'machine_type': 'winding',
             'manufacturer': 'Autoconer', 'model_name': 'X6', 'year_installed': 2021,
             'location': 'سالن تکمیل', 'production_line': line2},
            {'code': 'TF-02', 'name': 'دولاتابی دو', 'machine_type': 'tfo',
             'manufacturer': 'Volkmann', 'model_name': 'VTS 08', 'year_installed': 2021,
             'location': 'سالن تکمیل', 'production_line': line2},
            {'code': 'HS-02', 'name': 'هیت‌ست دو', 'machine_type': 'heatset',
             'manufacturer': 'Superba', 'model_name': 'V008', 'year_installed': 2021,
             'location': 'سالن تکمیل', 'production_line': line2},
        ]

        for data in machines_data:
            if not Machine.objects.filter(code=data['code']).exists():
                m = Machine.objects.create(**data)
                self.stdout.write(f'  ماشین: {m.code} - {m.name}')

    # ══════════════════════════════════════════════════════
    # SHIFTS
    # ══════════════════════════════════════════════════════

    def _create_shifts(self):
        from apps.core.models import Shift, ProductionLine, LineShiftAssignment
        from apps.accounts.models import User
        from datetime import time

        supervisors = list(User.objects.filter(role='supervisor'))

        shifts_data = [
            {'name': 'صبح', 'code': 'L1-A', 'start_time': time(6, 0), 'end_time': time(14, 0)},
            {'name': 'عصر', 'code': 'L1-B', 'start_time': time(14, 0), 'end_time': time(22, 0)},
            {'name': 'شب', 'code': 'L1-C', 'start_time': time(22, 0), 'end_time': time(6, 0)},
            {'name': 'صبح', 'code': 'L2-A', 'start_time': time(6, 0), 'end_time': time(14, 0)},
            {'name': 'عصر', 'code': 'L2-B', 'start_time': time(14, 0), 'end_time': time(22, 0)},
            {'name': 'شب', 'code': 'L2-C', 'start_time': time(22, 0), 'end_time': time(6, 0)},
        ]

        for i, data in enumerate(shifts_data):
            if not Shift.objects.filter(code=data['code']).exists():
                line_num = 1 if 'L1' in data['code'] else 2
                line = ProductionLine.objects.get(code=f'LINE-0{line_num}')
                shift = Shift.objects.create(production_line=line, **data)
                # اختصاص سرشیفت
                sup = supervisors[i % len(supervisors)] if supervisors else None
                LineShiftAssignment.objects.create(
                    production_line=line, shift=shift, supervisor=sup
                )
                self.stdout.write(f'  شیفت: {shift.code} → {sup}')

    # ══════════════════════════════════════════════════════
    # INVENTORY
    # ══════════════════════════════════════════════════════

    def _create_inventory(self):
        from apps.inventory.models import FiberCategory, FiberStock, DyeStock, ChemicalStock

        # دسته‌بندی الیاف
        categories = [
            {'code': 'PES', 'name': 'پلی‌استر'},
            {'code': 'ACR', 'name': 'اکریلیک'},
            {'code': 'VIS', 'name': 'ویسکوز'},
            {'code': 'PP', 'name': 'پلی‌پروپیلن'},
        ]
        for cat_data in categories:
            FiberCategory.objects.get_or_create(code=cat_data['code'], defaults={'name': cat_data['name']})

        # الیاف
        fibers = [
            ('PES', 'FB-PES-001', 'ایران یارن', 1.5, 38, 4500, '#e8e8e8'),
            ('PES', 'FB-PES-002', 'ایران یارن', 1.5, 38, 3800, '#e8e8e8'),
            ('ACR', 'FB-ACR-001', 'آکساChem', 2.0, 60, 2200, '#f5f5f5'),
            ('ACR', 'FB-ACR-002', 'آکساChem', 3.0, 60, 1800, '#f0f0f0'),
            ('VIS', 'FB-VIS-001', 'لنزینگ', 1.3, 38, 900, '#fafafa'),
            ('PP', 'FB-PP-001', 'پتروشیمی', 2.0, 51, 1500, '#e5e5e5'),
        ]
        for cat_code, batch, supplier, denier, staple, weight, _ in fibers:
            cat = FiberCategory.objects.get(code=cat_code)
            if not FiberStock.objects.filter(batch_number=batch).exists():
                FiberStock.objects.create(
                    category=cat,
                    batch_number=batch,
                    supplier=supplier,
                    denier=denier,
                    staple_length=staple,
                    initial_weight=weight,
                    current_weight=weight * Decimal('0.65'),
                    received_date=date.today() - timedelta(days=random.randint(5, 30)),
                    quality_grade=random.choice(['A', 'A', 'A', 'B']),
                    warehouse_loc=f'ردیف {random.randint(1, 5)} - قفسه {random.choice(["الف", "ب", "ج"])}',
                    unit_price=random.randint(280000, 350000),
                )

        # رنگ‌ها
        dyes = [
            ('DY-001', 'قرمز کارمین', 'reactive', 'قرمز', 150, '#DC143C'),
            ('DY-002', 'آبی تیره', 'reactive', 'آبی', 120, '#00008B'),
            ('DY-003', 'سبز زمرد', 'disperse', 'سبز', 80, '#50C878'),
            ('DY-004', 'زرد طلایی', 'acid', 'زرد', 60, '#FFD700'),
            ('DY-005', 'قهوه‌ای شکلاتی', 'reactive', 'قهوه‌ای', 200, '#7B3F00'),
            ('DY-006', 'کرم عاجی', 'disperse', 'کرم', 90, '#FFFDD0'),
        ]
        for code, name, dye_type, family, weight, _ in dyes:
            if not DyeStock.objects.filter(code=code).exists():
                DyeStock.objects.create(
                    code=code, name=name, dye_type=dye_type, color_family=family,
                    batch_number=f'LOT-{code}',
                    manufacturer='دایستار',
                    initial_weight=weight, current_weight=weight * Decimal('0.7'),
                    received_date=date.today() - timedelta(days=random.randint(3, 20)),
                    expiry_date=date.today() + timedelta(days=365),
                    unit_price=random.randint(1200000, 1800000),
                )

        # مواد شیمیایی
        chemicals = [
            ('CH-001', 'اسید استیک ۵۰%', 'acid', 50, 500),
            ('CH-002', 'کربنات سدیم', 'alkali', None, 300),
            ('CH-003', 'نمک طعام', 'salt', None, 800),
            ('CH-004', 'نرم‌کننده کاتیونی', 'softener', None, 150),
            ('CH-005', 'تثبیت‌کننده UV', 'fixative', None, 80),
        ]
        for code, name, chem_type, conc, amount in chemicals:
            if not ChemicalStock.objects.filter(code=code).exists():
                ChemicalStock.objects.create(
                    code=code, name=name, chemical_type=chem_type,
                    batch_number=f'LOT-{code}',
                    concentration=conc,
                    initial_amount=amount, current_amount=amount * Decimal('0.6'),
                    received_date=date.today() - timedelta(days=10),
                    expiry_date=date.today() + timedelta(days=180),
                    unit_price=random.randint(50000, 200000),
                )
        self.stdout.write('  موجودی انبار ایجاد شد.')

    # ══════════════════════════════════════════════════════
    # CUSTOMERS & ORDERS
    # ══════════════════════════════════════════════════════

    def _create_customers(self):
        from apps.orders.models import Customer

        customers_data = [
            {'name': 'احمد کریمی', 'company': 'کارپت کریمی اصفهان',
             'phone': '03132001100', 'mobile': '09131001100',
             'city': 'اصفهان', 'province': 'اصفهان', 'credit_limit': 5000000000},
            {'name': 'محمود رضایی', 'company': 'فرش ماشینی رضایی کاشان',
             'phone': '03155001200', 'mobile': '09131002200',
             'city': 'کاشان', 'province': 'اصفهان', 'credit_limit': 3000000000},
            {'name': 'حسین نوروزی', 'company': 'تولیدی نخ نوروزی تبریز',
             'phone': '04133001300', 'mobile': '09141003300',
             'city': 'تبریز', 'province': 'آذربایجان شرقی', 'credit_limit': 4000000000},
            {'name': 'علی اکبر صادقی', 'company': 'گروه فرش صادقی مشهد',
             'phone': '05138001400', 'mobile': '09151004400',
             'city': 'مشهد', 'province': 'خراسان رضوی', 'credit_limit': 6000000000},
            {'name': 'فاطمه موسوی', 'company': 'بافت ابریشم تهران',
             'phone': '02122001500', 'mobile': '09121005500',
             'city': 'تهران', 'province': 'تهران', 'credit_limit': 2500000000},
        ]

        for data in customers_data:
            if not Customer.objects.filter(phone=data['phone']).exists():
                c = Customer.objects.create(**data)
                self.stdout.write(f'  مشتری: {c.name}')

    def _create_color_shades(self):
        from apps.orders.models import ColorShade
        from apps.accounts.models import User

        approver = User.objects.filter(role='manager').first()

        shades = [
            ('SH-1001', 'قرمز ایرانی', '#C0392B'),
            ('SH-1002', 'آبی لاجوردی', '#1A237E'),
            ('SH-1003', 'سبز ترکی', '#1B5E20'),
            ('SH-1004', 'زرد گندمی', '#F9A825'),
            ('SH-1005', 'قهوه‌ای نیمه‌تاریک', '#4E342E'),
            ('SH-1006', 'سفید شیری', '#FAFAFA'),
            ('SH-1007', 'کرم عاج', '#FFF9C4'),
            ('SH-1008', 'نارنجی خزان', '#E65100'),
        ]

        for code, name, hex_color in shades:
            if not ColorShade.objects.filter(code=code).exists():
                ColorShade.objects.create(
                    code=code, name=name, color_hex=hex_color,
                    is_approved=True,
                    approved_by=approver,
                    approved_at=timezone.now() - timedelta(days=random.randint(10, 60)),
                )

    def _create_orders(self):
        from apps.orders.models import Order, Customer, ColorShade
        from apps.core.models import ProductionLine
        from apps.accounts.models import User

        customers = list(Customer.objects.all())
        shades = list(ColorShade.objects.all())
        lines = list(ProductionLine.objects.all())
        creator = User.objects.filter(role='manager').first()

        if not customers or not creator:
            return

        yarn_types = ['نخ فرش پلی‌استر', 'نخ فرش اکریلیک', 'نخ فرش مخلوط PES/ACR']
        yarn_counts = ['1400 دنیر/2', '1000 دنیر/2', '800 دنیر/2', '600 دنیر/2']
        statuses = ['confirmed', 'in_production', 'in_production', 'quality_check', 'ready', 'delivered']

        today = date.today()
        for i in range(15):
            order_date = today - timedelta(days=random.randint(0, 45))
            order_num = f"ORD-{order_date.strftime('%Y%m%d')}-{i+1:03d}"

            if Order.objects.filter(order_number=order_num).exists():
                continue

            status = statuses[i % len(statuses)]
            qty = Decimal(str(random.randint(500, 3000)))
            price = Decimal(str(random.randint(380000, 450000)))

            Order.objects.create(
                order_number=order_num,
                customer=random.choice(customers),
                color_shade=random.choice(shades) if shades else None,
                production_line=random.choice(lines),
                yarn_type=random.choice(yarn_types),
                yarn_count=random.choice(yarn_counts),
                quantity_kg=qty,
                unit_price=price,
                total_price=qty * price,
                delivery_date=today + timedelta(days=random.randint(-10, 30)),
                priority=random.choice(['normal', 'normal', 'high', 'urgent']),
                status=status,
                progress_pct=random.randint(0, 100) if status == 'in_production' else (
                    100 if status in ('ready', 'delivered') else 0),
                ply_count=2,
                heatset_required=True,
                process_sequence='no_dye',
                created_by=creator,
            )
        self.stdout.write('  سفارشات ایجاد شدند.')

    # ══════════════════════════════════════════════════════
    # MAINTENANCE SCHEDULES
    # ══════════════════════════════════════════════════════

    def _create_maintenance_schedules(self):
        from apps.maintenance.models import Schedule, WorkOrder, DowntimeLog, MachineServiceDate
        from apps.core.models import Machine, Shift
        from apps.accounts.models import User

        machines = list(Machine.objects.all())
        tech = User.objects.filter(department='maintenance').first()
        operator = User.objects.filter(role='operator').first()
        shifts = list(Shift.objects.all())

        if not machines or not operator:
            return

        for machine in machines:
            # PM schedule
            Schedule.objects.get_or_create(
                machine=machine,
                title=f'سرویس هفتگی {machine.code}',
                defaults={
                    'maintenance_type': 'preventive',
                    'frequency': 'weekly',
                    'description': f'تمیزکاری، روغن‌کاری و بازرسی ماشین {machine.name}',
                    'next_due_at': timezone.now() + timedelta(days=random.randint(-3, 10)),
                    'assigned_to': tech,
                    'priority': 'medium',
                }
            )

            # WO برای بعضی ماشین‌ها
            if random.random() > 0.5:
                wo_num = f"WO-{date.today().strftime('%Y%m%d')}-{machine.id:03d}"
                WorkOrder.objects.get_or_create(
                    wo_number=wo_num,
                    defaults={
                        'machine': machine,
                        'title': f'بازرسی و تعمیر {machine.name}',
                        'wo_type': random.choice(['preventive', 'corrective']),
                        'priority': random.choice(['low', 'medium', 'high']),
                        'status': random.choice(['open', 'in_progress', 'completed']),
                        'reported_by': operator,
                        'assigned_to': tech,
                        'cost_parts': random.randint(0, 5000000),
                        'cost_labor': random.randint(500000, 2000000),
                        'downtime_min': random.randint(30, 240),
                    }
                )

            # لاگ توقف
            if random.random() > 0.4 and shifts:
                start = timezone.now() - timedelta(hours=random.randint(2, 48))
                end = start + timedelta(minutes=random.randint(15, 180))
                DowntimeLog.objects.create(
                    machine=machine,
                    operator=operator,
                    shift=random.choice(shifts),
                    start_time=start,
                    end_time=end,
                    duration_min=int((end - start).total_seconds() / 60),
                    reason_category=random.choice(['mechanical', 'electrical', 'material', 'planned']),
                    reason_detail=random.choice([
                        'گیر کردن مواد در مسیر',
                        'قطع برق موقت',
                        'تعویض شیطانک',
                        'سرویس روتین',
                        'کمبود مواد اولیه',
                        'بازرسی کنترل کیفیت',
                    ]),
                    production_loss=Decimal(str(round(random.uniform(10, 150), 2))),
                )

        self.stdout.write('  برنامه‌های نگهداری ایجاد شدند.')

    # ══════════════════════════════════════════════════════
    # HOURLY BATCHES (اجرا هر ساعت با cron)
    # ══════════════════════════════════════════════════════

    def _generate_hourly_batches(self):
        """هر ساعت یک‌بار: بچ‌های جدید تولید به هر خط اضافه می‌شود"""
        from apps.core.models import Machine, Shift, ProductionLine
        from apps.accounts.models import User
        from apps.orders.models import Order

        lines = list(ProductionLine.objects.filter(status='active'))
        operators = list(User.objects.filter(role='operator', is_active=True))
        orders = list(Order.objects.filter(status='in_production'))

        if not lines or not operators:
            self.stdout.write(self.style.WARNING('  داده پایه کافی نیست. ابتدا --reset اجرا کنید.'))
            return

        for line in lines:
            shift = self._get_current_shift(line)
            if not shift:
                continue

            operator = random.choice(operators)
            order = random.choice(orders) if orders else None
            today = date.today()

            # بچ حلاجی
            self._create_blowroom_batch(line, shift, operator, order, today)
            # بچ کاردینگ
            self._create_carding_batch(line, shift, operator, order, today)
            # بچ پاساژ
            self._create_passage_batch(line, shift, operator, order, today)
            # بچ فینیشر
            self._create_finisher_batch(line, shift, operator, order, today)
            # بچ‌های رینگ
            self._create_spinning_batch(line, shift, operator, order, today)
            # بچ‌های بوبین‌پیچی
            self._create_winding_batch(line, shift, operator, order, today)
            # بچ دولاتابی
            self._create_tfo_batch(line, shift, operator, order, today)
            # بچ هیت‌ست
            self._create_heatset_batch(line, shift, operator, order, today)
            # توقف تصادفی
            if random.random() > 0.7:
                self._create_downtime(line, shift, operator)

        self.stdout.write('  بچ‌های ساعتی ایجاد شدند.')

    def _get_current_shift(self, line):
        from apps.core.models import Shift
        from datetime import time as dtime
        now = datetime.now().time()
        shifts = Shift.objects.filter(production_line=line, is_active=True)
        for shift in shifts:
            s, e = shift.start_time, shift.end_time
            if s < e:
                if s <= now < e:
                    return shift
            else:  # شب‌کاری
                if now >= s or now < e:
                    return shift
        return shifts.first()

    def _make_batch_num(self, prefix):
        """شماره بچ منحصربفرد"""
        import time as tmod
        ts = str(int(tmod.time() * 1000))[-6:]
        return f"{prefix}-{date.today().strftime('%Y%m%d')}-{ts}"

    def _create_carding_batch(self, line, shift, operator, order, today):
        from apps.carding.models import Production
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='carding', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        input_w = Decimal(str(round(random.uniform(200, 400), 2)))
        waste_pct = Decimal(str(round(random.uniform(3, 6), 2)))
        output_w = input_w * (1 - waste_pct / 100)

        Production.objects.create(
            batch_number=self._make_batch_num('CR'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            speed_rpm=Decimal(str(random.randint(300, 500))),
            sliver_count=Decimal('5.0'),
            sliver_weight_gperm=Decimal('5.0'),
            input_weight=input_w,
            output_weight=output_w,
            waste_weight=input_w - output_w,
            waste_pct=waste_pct,
            neps_count=random.randint(50, 200),
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 3)),
        )

    def _create_passage_batch(self, line, shift, operator, order, today):
        from apps.passage.models import Production, Input as PInput
        from apps.core.models import Machine
        from apps.carding.models import Production as CrProd

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='passage', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        input_w = Decimal(str(round(random.uniform(150, 350), 2)))
        output_w = input_w * Decimal('0.97')
        num_inputs = random.randint(6, 8)

        prod = Production.objects.create(
            batch_number=self._make_batch_num('PS'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            passage_number=random.choice([1, 2]),
            num_inputs=num_inputs,
            draft_ratio=Decimal(str(round(random.uniform(5.5, 8.0), 3))),
            output_sliver_count=Decimal('5.0'),
            input_total_weight=input_w,
            output_weight=output_w,
            speed_mpm=Decimal(str(round(random.uniform(300, 600), 1))),
            evenness_cv=Decimal(str(round(random.uniform(2.5, 5.0), 2))),
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 3)),
        )
        # ورودی‌های پاساژ
        cr_batches = list(CrProd.objects.filter(
            production_line=line).order_by('-created_at')[:num_inputs])
        for i, cr in enumerate(cr_batches[:num_inputs], 1):
            PInput.objects.create(
                passage_production=prod,
                input_position=i,
                source_type='carding',
                source_id=cr.id,
                source_batch_number=cr.batch_number,
                weight_used=input_w / num_inputs,
            )

    def _create_finisher_batch(self, line, shift, operator, order, today):
        from apps.finisher.models import Production
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='finisher', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        input_w = Decimal(str(round(random.uniform(100, 250), 2)))
        output_w = input_w * Decimal('0.98')

        Production.objects.create(
            batch_number=self._make_batch_num('FN'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            draft_ratio=Decimal(str(round(random.uniform(6.0, 10.0), 3))),
            twist_tpm=Decimal(str(round(random.uniform(0.8, 1.5), 2))),
            output_sliver_count=Decimal('0.6'),
            speed_mpm=Decimal(str(round(random.uniform(15, 30), 1))),
            input_weight=input_w,
            output_weight=output_w,
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 3)),
        )

    def _create_blowroom_batch(self, line, shift, operator, order, today):
        from apps.blowroom.models import Batch, BatchInput
        from apps.core.models import Machine
        from apps.inventory.models import FiberStock

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='blowroom', status='active'))
        fibers = list(FiberStock.objects.filter(
            status='available', current_weight__gt=100))

        if not machines or not fibers:
            return

        machine = random.choice(machines)
        input_weight = Decimal(str(round(random.uniform(300, 600), 2)))
        waste_pct = Decimal(str(round(random.uniform(1.5, 4.0), 2)))
        output = input_weight * (1 - waste_pct / 100)

        batch = Batch.objects.create(
            batch_number=self._make_batch_num('BL'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            total_input_weight=input_weight,
            output_weight=output,
            waste_weight=input_weight - output,
            waste_pct=waste_pct,
            blend_recipe={'PES': 70, 'ACR': 30},
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 2)),
        )
        # ورودی‌های بچ
        fiber = random.choice(fibers)
        BatchInput.objects.create(
            batch=batch, fiber_stock=fiber,
            weight_used=input_weight, percentage=100,
        )

    def _create_spinning_batch(self, line, shift, operator, order, today):
        from apps.spinning.models import Production
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='ring', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        output = Decimal(str(round(random.uniform(80, 200), 2)))

        Production.objects.create(
            batch_number=self._make_batch_num('RG'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            spindle_speed_rpm=random.randint(9000, 12000),
            twist_tpm=Decimal(str(round(random.uniform(180, 280), 1))),
            twist_direction=random.choice(['S', 'Z']),
            yarn_count=Decimal('14.50'),
            traveler_number=f'6/0 {random.choice(["SS", "HO"])}',
            input_weight=output * Decimal('1.02'),
            output_weight=output,
            num_spindles_active=random.randint(400, 480),
            num_spindles_total=480,
            breakage_count=random.randint(2, 25),
            efficiency_pct=Decimal(str(round(random.uniform(78, 95), 1))),
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 3)),
        )

    def _create_winding_batch(self, line, shift, operator, order, today):
        from apps.winding.models import Production
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='winding', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        input_w = Decimal(str(round(random.uniform(100, 250), 2)))
        waste = input_w * Decimal('0.015')
        output_w = input_w - waste
        packages = int(output_w / Decimal('2.5'))

        Production.objects.create(
            batch_number=self._make_batch_num('WD'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            input_weight_kg=input_w,
            output_weight_kg=output_w,
            waste_weight_kg=waste,
            output_packages=packages,
            package_weight_kg=Decimal('2.5'),
            package_type='cone',
            winding_speed_mpm=Decimal(str(random.randint(1000, 1800))),
            cuts_per_100km=random.randint(5, 35),
            splices_per_100km=random.randint(5, 35),
            efficiency_pct=Decimal(str(round(random.uniform(82, 96), 1))),
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 2)),
        )

    def _create_tfo_batch(self, line, shift, operator, order, today):
        from apps.tfo.models import Production
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='tfo', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        input_w = Decimal(str(round(random.uniform(150, 350), 2)))
        output_w = input_w * Decimal('0.98')

        Production.objects.create(
            batch_number=self._make_batch_num('TF'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['in_progress', 'completed', 'completed']),
            ply_count=2,
            twist_tpm=Decimal(str(round(random.uniform(200, 350), 1))),
            twist_direction=random.choice(['S', 'Z']),
            spindle_speed_rpm=random.randint(5000, 8000),
            input_packages=random.randint(60, 120),
            input_weight_kg=input_w,
            output_packages=random.randint(30, 60),
            output_weight_kg=output_w,
            waste_weight_kg=input_w - output_w,
            breakage_count=random.randint(0, 15),
            efficiency_pct=Decimal(str(round(random.uniform(80, 95), 1))),
            started_at=timezone.now() - timedelta(hours=random.uniform(0.5, 2)),
        )

    def _create_heatset_batch(self, line, shift, operator, order, today):
        from apps.heatset.models import Batch as HSBatch
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(
            production_line=line, machine_type='heatset', status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        weight = Decimal(str(round(random.uniform(200, 400), 2)))
        packages = int(weight / Decimal('2.5'))
        dur = random.randint(45, 90)
        started = timezone.now() - timedelta(hours=random.uniform(0.5, 2))

        HSBatch.objects.create(
            batch_number=self._make_batch_num('HS'),
            production_line=line,
            machine=machine,
            operator=operator,
            shift=shift,
            order=order,
            production_date=today,
            status=random.choice(['processing', 'completed', 'completed']),
            machine_type_hs='superba',
            fiber_type=random.choice(['polyester', 'acrylic']),
            cycle_type='standard',
            temperature_c=Decimal(str(round(random.uniform(115, 135), 1))),
            steam_pressure_bar=Decimal(str(round(random.uniform(1.2, 2.0), 2))),
            vacuum_level_mbar=Decimal(str(round(random.uniform(80, 150), 1))),
            pre_heat_min=10,
            vacuum_time_min=8,
            steam_time_min=random.randint(20, 40),
            dwell_time_min=random.randint(10, 20),
            cooldown_min=15,
            batch_weight_kg=weight,
            packages_count=packages,
            quality_result=random.choice(['pass', 'pass', 'pass', 'conditional']),
            shrinkage_pct=Decimal(str(round(random.uniform(0.5, 2.5), 2))),
            twist_stability=random.choice(['excellent', 'good', 'good']),
            started_at=started,
            completed_at=started + timedelta(minutes=dur),
        )

    def _create_downtime(self, line, shift, operator):
        from apps.maintenance.models import DowntimeLog
        from apps.core.models import Machine

        machines = list(Machine.objects.filter(production_line=line, status='active'))
        if not machines:
            return

        machine = random.choice(machines)
        dur = random.randint(10, 90)
        start = timezone.now() - timedelta(minutes=dur + random.randint(0, 30))
        end = start + timedelta(minutes=dur)

        DowntimeLog.objects.create(
            machine=machine,
            operator=operator,
            shift=shift,
            production_line=line,
            start_time=start,
            end_time=end,
            duration_min=dur,
            reason_category=random.choice(['mechanical', 'electrical', 'material', 'operator', 'planned']),
            reason_detail=random.choice([
                'گیر کردن نخ',
                'تعویض بوبین',
                'تنظیم تنش نخ',
                'سرویس روتین',
                'انتقال مواد',
                'استراحت اپراتور',
            ]),
            production_loss=Decimal(str(round(random.uniform(5, 80), 2))),
        )
