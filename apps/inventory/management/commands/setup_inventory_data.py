"""
Diaco MES - Setup Sample Inventory & Orders Data
===================================================
ساخت داده‌های نمونه انبار و سفارشات برای تست.

Usage:
    python manage.py setup_inventory_data
"""
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.inventory.models import FiberCategory, FiberStock, DyeStock, ChemicalStock
from apps.orders.models import Customer, ColorShade, Order

User = get_user_model()


class Command(BaseCommand):
    help = 'ساخت داده‌های نمونه انبار و سفارشات'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n═══ دیاکو - داده نمونه انبار و سفارشات ═══\n'))

        admin = User.objects.filter(role='admin').first()
        if not admin:
            self.stdout.write(self.style.ERROR('ابرکاربر یافت نشد! اول setup_initial_data را اجرا کنید.'))
            return

        self._create_fiber_categories()
        self._create_fiber_stocks()
        self._create_dye_stocks()
        self._create_chemical_stocks()
        self._create_customers()
        self._create_color_shades(admin)
        self._create_orders(admin)

        self.stdout.write(self.style.SUCCESS('\n✅ داده‌های نمونه با موفقیت ایجاد شدند!\n'))

    def _create_fiber_categories(self):
        data = [
            {'name': 'پلی‌استر', 'code': 'PES'},
            {'name': 'اکریلیک', 'code': 'ACR'},
            {'name': 'ویسکوز', 'code': 'VIS'},
            {'name': 'پشم', 'code': 'WOL'},
            {'name': 'پنبه', 'code': 'COT'},
            {'name': 'نایلون', 'code': 'NYL'},
        ]
        for d in data:
            obj, created = FiberCategory.objects.get_or_create(code=d['code'], defaults=d)
            if created:
                self.stdout.write(f'  ✓ دسته الیاف «{obj.name}»')

    def _create_fiber_stocks(self):
        today = date.today()
        pes = FiberCategory.objects.get(code='PES')
        acr = FiberCategory.objects.get(code='ACR')
        vis = FiberCategory.objects.get(code='VIS')

        stocks = [
            {'category': pes, 'batch_number': 'FB-14041101-001', 'supplier': 'شرکت الیاف سپاهان',
             'color_raw': 'سفید', 'denier': Decimal('1.5'), 'staple_length': Decimal('38'),
             'initial_weight': Decimal('5000'), 'current_weight': Decimal('4200'),
             'unit_price': Decimal('850000'), 'received_date': today - timedelta(days=30),
             'warehouse_loc': 'ردیف ۱ - قفسه الف', 'quality_grade': 'A'},
            {'category': pes, 'batch_number': 'FB-14041105-002', 'supplier': 'الیاف تبریز',
             'color_raw': 'اکرو', 'denier': Decimal('2.0'), 'staple_length': Decimal('51'),
             'initial_weight': Decimal('3000'), 'current_weight': Decimal('3000'),
             'unit_price': Decimal('780000'), 'received_date': today - timedelta(days=15),
             'warehouse_loc': 'ردیف ۱ - قفسه ب', 'quality_grade': 'A'},
            {'category': acr, 'batch_number': 'FB-14041110-003', 'supplier': 'اکریلان ایران',
             'color_raw': 'سفید', 'denier': Decimal('3.0'), 'staple_length': Decimal('76'),
             'initial_weight': Decimal('2000'), 'current_weight': Decimal('1500'),
             'unit_price': Decimal('920000'), 'received_date': today - timedelta(days=45),
             'warehouse_loc': 'ردیف ۲ - قفسه الف', 'quality_grade': 'B'},
            {'category': vis, 'batch_number': 'FB-14041120-004', 'supplier': 'ویسکوز قائم‌شهر',
             'color_raw': 'سفید', 'denier': Decimal('1.2'), 'staple_length': Decimal('38'),
             'initial_weight': Decimal('1500'), 'current_weight': Decimal('1500'),
             'unit_price': Decimal('1100000'), 'received_date': today - timedelta(days=5),
             'warehouse_loc': 'ردیف ۳ - قفسه الف', 'quality_grade': 'A'},
        ]

        for d in stocks:
            obj, created = FiberStock.objects.get_or_create(
                batch_number=d['batch_number'], defaults=d
            )
            if created:
                self.stdout.write(f'  ✓ الیاف «{obj.batch_number}» ({obj.category.name})')

    def _create_dye_stocks(self):
        today = date.today()
        dyes = [
            {'name': 'قرمز راکتیو R-3BS', 'code': 'DY-R3BS-001', 'color_family': 'قرمز',
             'dye_type': 'reactive', 'manufacturer': 'Huntsman',
             'batch_number': 'HU-2024-R001', 'initial_weight': Decimal('50'),
             'current_weight': Decimal('42'), 'unit': 'kg',
             'unit_price': Decimal('3500000'), 'received_date': today - timedelta(days=60)},
            {'name': 'آبی دیسپرس D-BL', 'code': 'DY-DBL-002', 'color_family': 'آبی',
             'dye_type': 'disperse', 'manufacturer': 'DyStar',
             'batch_number': 'DS-2024-B002', 'initial_weight': Decimal('30'),
             'current_weight': Decimal('28'), 'unit': 'kg',
             'unit_price': Decimal('4200000'), 'received_date': today - timedelta(days=40)},
            {'name': 'زرد اسیدی A-YL', 'code': 'DY-AYL-003', 'color_family': 'زرد',
             'dye_type': 'acid', 'manufacturer': 'Archroma',
             'batch_number': 'AR-2024-Y003', 'initial_weight': Decimal('25'),
             'current_weight': Decimal('25'), 'unit': 'kg',
             'unit_price': Decimal('2800000'), 'received_date': today - timedelta(days=10)},
        ]
        for d in dyes:
            obj, created = DyeStock.objects.get_or_create(code=d['code'], defaults=d)
            if created:
                self.stdout.write(f'  ✓ رنگ «{obj.name}»')

    def _create_chemical_stocks(self):
        today = date.today()
        chemicals = [
            {'name': 'اسید استیک', 'code': 'CH-AA-001', 'chemical_type': 'acid',
             'manufacturer': 'مرک', 'batch_number': 'MK-2024-001',
             'initial_amount': Decimal('200'), 'current_amount': Decimal('165'),
             'unit': 'liter', 'concentration': Decimal('30'),
             'unit_price': Decimal('180000'), 'received_date': today - timedelta(days=90)},
            {'name': 'سود سوزآور', 'code': 'CH-NaOH-002', 'chemical_type': 'alkali',
             'manufacturer': 'شیمی صنعت', 'batch_number': 'SS-2024-002',
             'initial_amount': Decimal('500'), 'current_amount': Decimal('380'),
             'unit': 'kg', 'concentration': Decimal('50'),
             'unit_price': Decimal('95000'), 'received_date': today - timedelta(days=60)},
            {'name': 'نمک صنعتی', 'code': 'CH-NaCl-003', 'chemical_type': 'salt',
             'manufacturer': 'نمک پارسیان', 'batch_number': 'NP-2024-003',
             'initial_amount': Decimal('1000'), 'current_amount': Decimal('750'),
             'unit': 'kg',
             'unit_price': Decimal('15000'), 'received_date': today - timedelta(days=30)},
            {'name': 'نرم‌کننده سیلیکونی', 'code': 'CH-SF-004', 'chemical_type': 'softener',
             'manufacturer': 'BASF', 'batch_number': 'BF-2024-004',
             'initial_amount': Decimal('100'), 'current_amount': Decimal('88'),
             'unit': 'kg',
             'unit_price': Decimal('2200000'), 'received_date': today - timedelta(days=20)},
        ]
        for d in chemicals:
            obj, created = ChemicalStock.objects.get_or_create(code=d['code'], defaults=d)
            if created:
                self.stdout.write(f'  ✓ ماده شیمیایی «{obj.name}»')

    def _create_customers(self):
        customers = [
            {'name': 'حسین رضایی', 'company': 'فرش کاشان نو', 'city': 'کاشان',
             'province': 'اصفهان', 'mobile': '09131234567', 'credit_limit': Decimal('500000000')},
            {'name': 'محمد احمدی', 'company': 'بافندگی احمدی', 'city': 'اصفهان',
             'province': 'اصفهان', 'mobile': '09139876543', 'credit_limit': Decimal('300000000')},
            {'name': 'علی محمودی', 'company': 'نساجی آریا', 'city': 'یزد',
             'province': 'یزد', 'mobile': '09137654321', 'credit_limit': Decimal('800000000')},
        ]
        for d in customers:
            obj, created = Customer.objects.get_or_create(
                mobile=d['mobile'], defaults=d
            )
            if created:
                self.stdout.write(f'  ✓ مشتری «{obj.name}» ({obj.company})')

    def _create_color_shades(self, admin):
        shades = [
            {'code': 'SH-1001', 'name': 'قرمز روناسی', 'color_hex': '#B22222',
             'is_approved': True, 'approved_by': admin,
             'recipe': {'dye_R3BS': 2.5, 'salt_NaCl': 40, 'soda_ash': 15}},
            {'code': 'SH-1002', 'name': 'آبی فیروزه‌ای', 'color_hex': '#40E0D0',
             'is_approved': True, 'approved_by': admin,
             'recipe': {'dye_DBL': 1.8, 'acid_acetic': 3, 'dispersant': 1}},
            {'code': 'SH-1003', 'name': 'سبز زمردی', 'color_hex': '#50C878',
             'is_approved': False,
             'recipe': {'dye_YL': 1.2, 'dye_DBL': 0.8, 'salt_NaCl': 35}},
        ]
        for d in shades:
            obj, created = ColorShade.objects.get_or_create(code=d['code'], defaults=d)
            if created:
                self.stdout.write(f'  ✓ شید رنگ «{obj.code} - {obj.name}»')

    def _create_orders(self, admin):
        today = date.today()
        cust1 = Customer.objects.first()
        cust2 = Customer.objects.last()
        shade1 = ColorShade.objects.get(code='SH-1001')
        shade2 = ColorShade.objects.get(code='SH-1002')

        orders = [
            {'order_number': 'ORD-14041201-001', 'customer': cust1, 'color_shade': shade1,
             'yarn_type': 'پلی‌استر تابیده', 'yarn_count': 'Ne 30/1',
             'quantity_kg': Decimal('500'), 'unit_price': Decimal('1200000'),
             'total_price': Decimal('600000000'), 'delivery_date': today + timedelta(days=30),
             'priority': 'high', 'status': 'in_production', 'progress_pct': 45,
             'created_by': admin},
            {'order_number': 'ORD-14041205-002', 'customer': cust2, 'color_shade': shade2,
             'yarn_type': 'اکریلیک HB', 'yarn_count': 'Nm 32/2',
             'quantity_kg': Decimal('1000'), 'unit_price': Decimal('950000'),
             'total_price': Decimal('950000000'), 'delivery_date': today + timedelta(days=45),
             'priority': 'normal', 'status': 'confirmed', 'progress_pct': 0,
             'created_by': admin},
            {'order_number': 'ORD-14041210-003', 'customer': cust1,
             'yarn_type': 'پشم مرینوس', 'yarn_count': 'Ne 20/1',
             'quantity_kg': Decimal('200'), 'delivery_date': today + timedelta(days=60),
             'priority': 'low', 'status': 'draft', 'progress_pct': 0,
             'created_by': admin},
        ]
        for d in orders:
            obj, created = Order.objects.get_or_create(
                order_number=d['order_number'], defaults=d
            )
            if created:
                self.stdout.write(f'  ✓ سفارش «{obj.order_number}» ({obj.customer.name})')
