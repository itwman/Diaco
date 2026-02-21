"""
Diaco MES — Demo Data Generator v3 (نهایی)
============================================
اجرا: python manage.py generate_demo [--reset] [--hourly] [--days N]
cron: هر ساعت یک‌بار  →  0 * * * *  python manage.py generate_demo --hourly

خطوط تولید:
  LINE-01  آکریلیک ۱  نخ فرش اکریلیک ۱۰۰۰ دنیر  ۶۵۰ kg/روز
  LINE-02  آکریلیک ۲  نخ فرش اکریلیک ۸۰۰  دنیر  ۵۰۰ kg/روز
  LINE-03  پلی‌استر    نخ فرش پلی‌استر ۱۴۰۰ دنیر  ۸۰۰ kg/روز
"""
import random
import time as _tmod
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

# اطلاعات ثابت خطوط
LINES = [
    {'code': 'LINE-01', 'fiber': 'acrylic',
     'name': 'خط آکریلیک ۱ — ۱۰۰۰ دنیر',
     'product': 'نخ فرش اکریلیک ۱۰۰۰ دنیر/۲ لا', 'capacity': 650},
    {'code': 'LINE-02', 'fiber': 'acrylic',
     'name': 'خط آکریلیک ۲ — ۸۰۰ دنیر',
     'product': 'نخ فرش اکریلیک ۸۰۰ دنیر/۲ لا',  'capacity': 500},
    {'code': 'LINE-03', 'fiber': 'polyester',
     'name': 'خط پلی‌استر — ۱۴۰۰ دنیر',
     'product': 'نخ فرش پلی‌استر ۱۴۰۰ دنیر/۲ لا', 'capacity': 800},
]


class Command(BaseCommand):
    help = 'تولید داده‌های دمو زنده — سیستم دیاکو MES'

    def add_arguments(self, parser):
        parser.add_argument('--reset',  action='store_true',
                            help='پاک‌سازی و شروع از صفر')
        parser.add_argument('--hourly', action='store_true',
                            help='فقط بچ‌های جدید ساعت جاری (cron)')
        parser.add_argument('--days', type=int, default=20,
                            help='روزهای تاریخچه (پیش‌فرض ۲۰)')

    def handle(self, *args, **opts):
        if opts['reset']:
            self.stdout.write('پاک‌سازی...')
            self._reset()

        if opts['hourly']:
            self._hourly()
        else:
            self._base_data()
            self._history(opts['days'])
            self._hourly()

        self.stdout.write(self.style.SUCCESS('✓ داده‌های دمو آماده شد!'))

    # ══════════════════════════════════════════════════════════════
    # RESET
    # ══════════════════════════════════════════════════════════════
    def _reset(self):
        from apps.blowroom.models  import Batch as BlB, BatchInput
        from apps.carding.models   import Production as CrP
        from apps.passage.models   import Production as PsP
        from apps.finisher.models  import Production as FnP
        from apps.spinning.models  import Production as SpP, TravelerReplacement
        from apps.winding.models   import Production as WdP
        from apps.tfo.models       import Production as TfP
        from apps.heatset.models   import Batch as HsB
        from apps.dyeing.models    import Batch as DyB
        from apps.maintenance.models import WorkOrder, DowntimeLog, Schedule, MachineServiceDate
        from apps.orders.models    import Order, Customer, ColorShade
        from apps.inventory.models import (FiberStock, DyeStock, ChemicalStock,
                                           StockTransaction, FiberCategory)
        from apps.core.models      import Machine, ProductionLine, Shift, LineShiftAssignment
        from apps.accounts.models  import User

        for m in [BatchInput, BlB, CrP, PsP, FnP, SpP, TravelerReplacement,
                  WdP, TfP, HsB, DyB, DowntimeLog, WorkOrder,
                  MachineServiceDate, Schedule,
                  Order, ColorShade, Customer,
                  StockTransaction, FiberStock, DyeStock, ChemicalStock, FiberCategory,
                  LineShiftAssignment, Shift, Machine, ProductionLine]:
            m.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('  ✓ پاک شد.')

    # ══════════════════════════════════════════════════════════════
    # BASE DATA
    # ══════════════════════════════════════════════════════════════
    def _base_data(self):
        self._users()
        self._lines()
        self._machines()
        self._shifts()
        self._inventory()
        self._customers()
        self._shades()
        self._orders()
        self._maintenance()

    # ── کاربران ───────────────────────────────────────────────────
    def _users(self):
        from apps.accounts.models import User
        data = [
            ('manager1',   'رضا',   'احمدی',    'manager',    'production', 'Demo@1404'),
            ('manager2',   'مریم',  'صادقی',    'manager',    'quality',    'Demo@1404'),
            ('sup_l1a',    'علی',   'محمدی',    'supervisor', 'production', 'Demo@1404'),
            ('sup_l1b',    'حسن',   'رضایی',    'supervisor', 'production', 'Demo@1404'),
            ('sup_l2a',    'زهرا',  'کریمی',    'supervisor', 'production', 'Demo@1404'),
            ('sup_l2b',    'امیر',  'حسینی',    'supervisor', 'production', 'Demo@1404'),
            ('sup_l3a',    'نگار',  'موسوی',    'supervisor', 'production', 'Demo@1404'),
            ('sup_l3b',    'کریم',  'اکبری',    'supervisor', 'production', 'Demo@1404'),
            ('op_blow1',   'محمد',  'حسینی',    'operator',   'production', 'Demo@1404'),
            ('op_card1',   'فاطمه', 'نجفی',     'operator',   'production', 'Demo@1404'),
            ('op_ring1',   'سعید',  'غلامی',    'operator',   'production', 'Demo@1404'),
            ('op_wind1',   'لیلا',  'جعفری',    'operator',   'production', 'Demo@1404'),
            ('op_tfo1',    'ناصر',  'عباسی',    'operator',   'production', 'Demo@1404'),
            ('op_hs1',     'نرگس',  'تهرانی',   'operator',   'production', 'Demo@1404'),
            ('op_ring2',   'رضا',   'قاسمی',    'operator',   'production', 'Demo@1404'),
            ('op_card2',   'مهدی',  'میرزایی',  'operator',   'production', 'Demo@1404'),
            ('tech1',      'کریم',  'پارسا',    'operator',   'maintenance','Demo@1404'),
            ('tech2',      'رحیم',  'قاسمی',    'operator',   'maintenance','Demo@1404'),
            ('warehouse1', 'ناصر',  'جعفری',    'operator',   'warehouse',  'Demo@1404'),
            ('viewer1',    'لیلا',  'تهرانی',   'viewer',     'office',     'Demo@1404'),
        ]
        for un, fn, ln, role, dept, pwd in data:
            if not User.objects.filter(username=un).exists():
                User.objects.create_user(
                    username=un, first_name=fn, last_name=ln,
                    role=role, department=dept, password=pwd)
        self.stdout.write('  ✓ کاربران')

    # ── خطوط تولید ───────────────────────────────────────────────
    def _lines(self):
        from apps.core.models import ProductionLine
        from apps.accounts.models import User
        mgr = User.objects.filter(role='manager').first()
        for ld in LINES:
            if not ProductionLine.objects.filter(code=ld['code']).exists():
                ProductionLine.objects.create(
                    code=ld['code'], name=ld['name'],
                    product_type=ld['product'],
                    target_capacity_kg=ld['capacity'],
                    line_manager=mgr)
        self.stdout.write('  ✓ خطوط تولید')

    # ── ماشین‌ها ─────────────────────────────────────────────────
    def _machines(self):
        from apps.core.models import Machine, ProductionLine
        l1 = ProductionLine.objects.get(code='LINE-01')
        l2 = ProductionLine.objects.get(code='LINE-02')
        l3 = ProductionLine.objects.get(code='LINE-03')

        ms = [
            # ── LINE-01  اکریلیک ۱ ────────────────────────────────
            ('BL-01','حلاجی خط۱',       'blowroom','Truetzschler','TC-19i', 2018,'سالن حلاجی',     l1),
            ('CR-01','کارد خط۱-۱',      'carding', 'Truetzschler','TC-30i', 2018,'سالن کاردینگ',   l1),
            ('CR-02','کارد خط۱-۲',      'carding', 'Truetzschler','TC-30i', 2019,'سالن کاردینگ',   l1),
            ('CR-03','کارد خط۱-۳',      'carding', 'Truetzschler','TC-30i', 2020,'سالن کاردینگ',   l1),
            ('PS-01','پاساژ خط۱-۱',     'passage', 'Rieter',      'RSB-D45',2018,'سالن پاساژ',     l1),
            ('PS-02','پاساژ خط۱-۲',     'passage', 'Rieter',      'RSB-D45',2019,'سالن پاساژ',     l1),
            ('FN-01','فینیشر خط۱-۱',    'finisher','Rieter',      'F 40',   2018,'سالن فینیشر',    l1),
            ('FN-02','فینیشر خط۱-۲',    'finisher','Rieter',      'F 40',   2019,'سالن فینیشر',    l1),
            ('RG-01','رینگ خط۱-۱',      'ring',    'Zinser',      '72XL',   2018,'سالن رینگ الف',  l1),
            ('RG-02','رینگ خط۱-۲',      'ring',    'Zinser',      '72XL',   2019,'سالن رینگ الف',  l1),
            ('RG-03','رینگ خط۱-۳',      'ring',    'Zinser',      '72XL',   2019,'سالن رینگ الف',  l1),
            ('RG-04','رینگ خط۱-۴',      'ring',    'Zinser',      '72XL',   2020,'سالن رینگ الف',  l1),
            ('WD-01','بوبین‌پیچ خط۱-۱', 'winding', 'Autoconer',   'X6',     2020,'سالن تکمیل',     l1),
            ('WD-02','بوبین‌پیچ خط۱-۲', 'winding', 'Autoconer',   'X6',     2021,'سالن تکمیل',     l1),
            ('TF-01','دولاتابی خط۱-۱',  'tfo',     'Volkmann',    'VTS 08', 2020,'سالن تکمیل',     l1),
            ('TF-02','دولاتابی خط۱-۲',  'tfo',     'Volkmann',    'VTS 08', 2021,'سالن تکمیل',     l1),
            ('HS-01','هیت‌ست خط۱',      'heatset', 'Superba',     'V008',   2020,'سالن تکمیل',     l1),
            # ── LINE-02  اکریلیک ۲ ────────────────────────────────
            ('BL-02','حلاجی خط۲',       'blowroom','Truetzschler','TC-19i', 2021,'سالن حلاجی',     l2),
            ('CR-04','کارد خط۲-۱',      'carding', 'Truetzschler','TC-30i', 2021,'سالن کاردینگ',   l2),
            ('CR-05','کارد خط۲-۲',      'carding', 'Truetzschler','TC-30i', 2022,'سالن کاردینگ',   l2),
            ('PS-03','پاساژ خط۲',       'passage', 'Rieter',      'RSB-D45',2021,'سالن پاساژ',     l2),
            ('FN-03','فینیشر خط۲',      'finisher','Rieter',      'F 40',   2021,'سالن فینیشر',    l2),
            ('RG-05','رینگ خط۲-۱',      'ring',    'Zinser',      '72XL',   2021,'سالن رینگ ب',   l2),
            ('RG-06','رینگ خط۲-۲',      'ring',    'Zinser',      '72XL',   2022,'سالن رینگ ب',   l2),
            ('RG-07','رینگ خط۲-۳',      'ring',    'Zinser',      '72XL',   2022,'سالن رینگ ب',   l2),
            ('WD-03','بوبین‌پیچ خط۲',   'winding', 'Autoconer',   'X6',     2021,'سالن تکمیل',     l2),
            ('TF-03','دولاتابی خط۲',    'tfo',     'Volkmann',    'VTS 08', 2021,'سالن تکمیل',     l2),
            ('HS-02','هیت‌ست خط۲',      'heatset', 'Superba',     'V008',   2021,'سالن تکمیل',     l2),
            # ── LINE-03  پلی‌استر ─────────────────────────────────
            ('BL-03','حلاجی PES',        'blowroom','Truetzschler','TC-19i', 2022,'سالن حلاجی',     l3),
            ('CR-06','کارد PES-1',       'carding', 'Truetzschler','TC-30i', 2022,'سالن کاردینگ',   l3),
            ('CR-07','کارد PES-2',       'carding', 'Truetzschler','TC-30i', 2022,'سالن کاردینگ',   l3),
            ('CR-08','کارد PES-3',       'carding', 'Truetzschler','TC-30i', 2023,'سالن کاردینگ',   l3),
            ('PS-04','پاساژ PES-1',      'passage', 'Rieter',      'RSB-D45',2022,'سالن پاساژ',     l3),
            ('PS-05','پاساژ PES-2',      'passage', 'Rieter',      'RSB-D45',2022,'سالن پاساژ',     l3),
            ('FN-04','فینیشر PES-1',     'finisher','Rieter',      'F 40',   2022,'سالن فینیشر',    l3),
            ('FN-05','فینیشر PES-2',     'finisher','Rieter',      'F 40',   2023,'سالن فینیشر',    l3),
            ('RG-08','رینگ PES-1',       'ring',    'Zinser',      '72XL',   2022,'سالن رینگ ج',   l3),
            ('RG-09','رینگ PES-2',       'ring',    'Zinser',      '72XL',   2022,'سالن رینگ ج',   l3),
            ('RG-10','رینگ PES-3',       'ring',    'Zinser',      '72XL',   2022,'سالن رینگ ج',   l3),
            ('RG-11','رینگ PES-4',       'ring',    'Zinser',      '351G',   2023,'سالن رینگ ج',   l3),
            ('WD-04','بوبین‌پیچ PES-1',  'winding', 'Autoconer',   'X6',     2022,'سالن تکمیل',     l3),
            ('WD-05','بوبین‌پیچ PES-2',  'winding', 'Autoconer',   'X6',     2022,'سالن تکمیل',     l3),
            ('TF-04','دولاتابی PES-1',   'tfo',     'Volkmann',    'VTS 08', 2022,'سالن تکمیل',     l3),
            ('TF-05','دولاتابی PES-2',   'tfo',     'Volkmann',    'VTS 08', 2023,'سالن تکمیل',     l3),
            ('HS-03','هیت‌ست PES-1',     'heatset', 'Superba',     'V008+',  2022,'سالن تکمیل',     l3),
            ('HS-04','هیت‌ست PES-2',     'heatset', 'Superba',     'V008+',  2023,'سالن تکمیل',     l3),
        ]
        for code,name,mtype,maker,model,year,loc,line in ms:
            if not Machine.objects.filter(code=code).exists():
                Machine.objects.create(
                    code=code, name=name, machine_type=mtype,
                    manufacturer=maker, model_name=model,
                    year_installed=year, location=loc,
                    production_line=line)
        self.stdout.write(f'  ✓ {len(ms)} ماشین')

    # ── شیفت‌ها ──────────────────────────────────────────────────
    def _shifts(self):
        from apps.core.models import Shift, ProductionLine, LineShiftAssignment
        from apps.accounts.models import User
        from datetime import time
        sups = list(User.objects.filter(role='supervisor'))
        idx = 0
        for lc in ['LINE-01','LINE-02','LINE-03']:
            line = ProductionLine.objects.get(code=lc)
            ln = lc[-2:]
            for sname, sfx, st, et in [
                ('صبح','A', time(6,0),  time(14,0)),
                ('عصر','B', time(14,0), time(22,0)),
                ('شب', 'C', time(22,0), time(6,0)),
            ]:
                code = f'L{ln}-{sfx}'
                if not Shift.objects.filter(code=code).exists():
                    shift = Shift.objects.create(
                        production_line=line, name=sname, code=code,
                        start_time=st, end_time=et)
                    sup = sups[idx % len(sups)] if sups else None
                    LineShiftAssignment.objects.create(
                        production_line=line, shift=shift, supervisor=sup)
                    idx += 1
        self.stdout.write('  ✓ شیفت‌ها')

    # ── موجودی ───────────────────────────────────────────────────
    def _inventory(self):
        from apps.inventory.models import (FiberCategory, FiberStock,
                                           DyeStock, ChemicalStock)

        for code,name in [('ACR','اکریلیک'),('PES','پلی‌استر'),
                           ('VIS','ویسکوز'),('PP','پلی‌پروپیلن')]:
            FiberCategory.objects.get_or_create(code=code, defaults={'name': name})

        fibers = [
            ('ACR','FB-ACR-001','آکسا کیمیا — ترکیه',       2.0,60,9000,'A'),
            ('ACR','FB-ACR-002','آکسا کیمیا — ترکیه',       2.0,60,6500,'A'),
            ('ACR','FB-ACR-003','دراکسلمایر — آلمان',       3.0,60,4200,'A'),
            ('ACR','FB-ACR-004','صنایع اکریلیک ایران',      2.0,60,3800,'B'),
            ('ACR','FB-ACR-005','آکسا کیمیا — ترکیه',       1.5,51,2500,'A'),
            ('PES','FB-PES-001','ایران یارن',                1.5,38,9500,'A'),
            ('PES','FB-PES-002','ایران یارن',                1.5,38,7800,'A'),
            ('PES','FB-PES-003','پلی‌اکریل ایران',          1.2,38,5200,'A'),
            ('PES','FB-PES-004','پتروشیمی اصفهان',          1.5,51,4500,'B'),
            ('VIS','FB-VIS-001','لنزینگ — اتریش',           1.3,38,1800,'A'),
            ('PP', 'FB-PP-001', 'پتروشیمی شازند',           2.0,51,2200,'B'),
        ]
        for cat_c,batch,supp,den,st,wt,gr in fibers:
            cat = FiberCategory.objects.get(code=cat_c)
            if not FiberStock.objects.filter(batch_number=batch).exists():
                FiberStock.objects.create(
                    category=cat, batch_number=batch, supplier=supp,
                    denier=den, staple_length=st,
                    initial_weight=wt,
                    current_weight=int(wt * random.uniform(0.35, 0.85)),
                    received_date=date.today()-timedelta(days=random.randint(3,45)),
                    quality_grade=gr,
                    warehouse_loc=f'ردیف {random.randint(1,6)}-قفسه {random.choice(["الف","ب","ج","د"])}',
                    unit_price=random.randint(220000,370000))

        dyes = [
            ('DY-001','قرمز کارمین',     'reactive','قرمز',      220),
            ('DY-002','قرمز گل‌رز',      'reactive','قرمز',      160),
            ('DY-003','آبی لاجوردی',     'reactive','آبی',       200),
            ('DY-004','آبی آسمانی',      'reactive','آبی',       130),
            ('DY-005','سبز زمردی',       'disperse','سبز',       110),
            ('DY-006','سبز شاه‌توتی',    'disperse','سبز',        85),
            ('DY-007','زرد طلایی',       'acid',    'زرد',        95),
            ('DY-008','نارنجی آتشین',    'acid',    'نارنجی',     75),
            ('DY-009','قهوه‌ای شکلاتی', 'reactive','قهوه‌ای',   270),
            ('DY-010','قهوه‌ای روشن',   'reactive','قهوه‌ای',   130),
            ('DY-011','کرم عاجی',        'disperse','کرم',       350),
            ('DY-012','سفید برفی',       'disperse','سفید',      420),
            ('DY-013','بنفش یاسی',       'acid',    'بنفش',       90),
            ('DY-014','خاکستری دودی',   'reactive','خاکستری',   170),
            ('DY-015','مشکی ذغالی',     'reactive','مشکی',      380),
            ('DY-016','فیروزه‌ای کاشان','disperse','فیروزه‌ای', 110),
        ]
        for code,name,dtype,fam,wt in dyes:
            if not DyeStock.objects.filter(code=code).exists():
                DyeStock.objects.create(
                    code=code, name=name, dye_type=dtype, color_family=fam,
                    batch_number=f'LOT-{code}-{date.today().strftime("%Y%m")}',
                    manufacturer=random.choice(['داستار','هانتسمن','دای‌استار','کلاریانت']),
                    initial_weight=wt,
                    current_weight=int(wt * random.uniform(0.3, 0.82)),
                    received_date=date.today()-timedelta(days=random.randint(5,50)),
                    expiry_date=date.today()+timedelta(days=random.randint(270,540)),
                    unit_price=random.randint(850000,2300000))

        chems = [
            ('CH-001','اسید استیک ۵۰٪',   'acid',    50,  550),
            ('CH-002','کربنات سدیم',       'alkali',  None,420),
            ('CH-003','نمک طعام',          'salt',    None,1300),
            ('CH-004','نرم‌کننده کاتیونی', 'softener',None,280),
            ('CH-005','تثبیت‌کننده UV',    'fixative',None,130),
            ('CH-006','پراکنده‌ساز',       'other',   None,320),
            ('CH-007','اسید فرمیک ۸۵٪',   'acid',    85,  220),
            ('CH-008','آنتی‌استاتیک',      'softener',None,195),
            ('CH-009','سود سوزآور',        'alkali',  None,380),
            ('CH-010','هیدروسولفیت سدیم', 'reducing',None,165),
        ]
        for code,name,ctype,conc,amt in chems:
            if not ChemicalStock.objects.filter(code=code).exists():
                ChemicalStock.objects.create(
                    code=code, name=name, chemical_type=ctype,
                    batch_number=f'LOT-{code}',
                    concentration=conc,
                    initial_amount=amt,
                    current_amount=amt*Decimal(str(round(random.uniform(0.28,0.78),2))),
                    received_date=date.today()-timedelta(days=random.randint(5,35)),
                    expiry_date=date.today()+timedelta(days=random.randint(90,400)),
                    unit_price=random.randint(38000,320000))
        self.stdout.write('  ✓ موجودی انبار')

    # ── مشتریان ─────────────────────────────────────────────────
    def _customers(self):
        from apps.orders.models import Customer
        rows = [
            # شرکت‌های فرش
            ('احمد کریمی',    'شرکت فرش ماشینی احمدی — کاشان',       '03155201100','09131001100','کاشان',       'اصفهان',         6_000_000_000),
            ('محمود رضایی',   'گروه فرش رضایی — اصفهان',              '03132001200','09131002200','اصفهان',      'اصفهان',         5_000_000_000),
            ('حسین نوروزی',   'فرش ماشینی نوروزی — تبریز',            '04133001300','09141003300','تبریز',       'آذربایجان شرقی', 4_500_000_000),
            ('علی‌اکبر صادقی','گروه فرش صادقی — مشهد',                '05138001400','09151004400','مشهد',        'خراسان رضوی',    7_000_000_000),
            ('فاطمه موسوی',   'بافت ابریشم — تهران',                  '02122001500','09121005500','تهران',       'تهران',          3_000_000_000),
            ('مهدی کریمی',    'فرش پارس — قم',                        '02537001600','09121006600','قم',          'قم',             2_500_000_000),
            ('جواد میرزایی',  'تولیدی فرش میرزایی — آران و بیدگل',   '03155801700','09131007700','آران و بیدگل','اصفهان',         2_000_000_000),
            ('نسرین احمدپور', 'گروه فرش ایران‌نخ — تهران',            '02122801800','09121008800','تهران',       'تهران',          4_000_000_000),
            ('کاظم علوی',     'کارخانه فرش علوی — کاشان',             '03155901900','09131009900','کاشان',       'اصفهان',         3_500_000_000),
            ('سارا طاهری',    'فرش ماشینی طاهری — اراک',              '08634002000','09181010000','اراک',        'مرکزی',          1_800_000_000),
            # شرکت‌های نخ
            ('رحیم قاسمی',    'نخ‌ریسی پارسیان — شاهین‌شهر',         '03145002100','09131011100','شاهین‌شهر',   'اصفهان',         3_500_000_000),
            ('سیما محمدزاده', 'نخ‌ریسی صنعتی محمدزاده — خمین',       '08643002200','09181012200','خمین',        'مرکزی',          2_800_000_000),
            ('بهروز دهقانی',  'تولیدی نخ دهقانی — یزد',              '03535002300','09131013300','یزد',         'یزد',            1_800_000_000),
            ('پریسا شریفی',   'گروه نخ صنعتی شریفی — اراک',          '08634002400','09181014400','اراک',        'مرکزی',          2_200_000_000),
            ('ابراهیم ملکی',  'نخ‌بافی صنعتی ملکی — کاشان',          '03155702500','09131015500','کاشان',       'اصفهان',         1_500_000_000),
        ]
        for name,company,phone,mobile,city,province,credit in rows:
            if not Customer.objects.filter(phone=phone).exists():
                Customer.objects.create(
                    name=name, company=company, phone=phone, mobile=mobile,
                    city=city, province=province, credit_limit=credit)
        self.stdout.write(f'  ✓ {len(rows)} مشتری')

    # ── شیدهای رنگ ──────────────────────────────────────────────
    def _shades(self):
        from apps.orders.models import ColorShade
        from apps.accounts.models import User
        approver = User.objects.filter(role='manager').first()
        shades = [
            ('SH-1001','قرمز ایرانی',       '#C0392B'),
            ('SH-1002','آبی لاجوردی',       '#1A237E'),
            ('SH-1003','سبز ترکی',          '#1B5E20'),
            ('SH-1004','زرد گندمی',         '#F9A825'),
            ('SH-1005','قهوه‌ای نیمه‌تاریک','#4E342E'),
            ('SH-1006','سفید شیری',         '#FAFAFA'),
            ('SH-1007','کرم عاج',           '#FFF9C4'),
            ('SH-1008','نارنجی خزان',       '#E65100'),
            ('SH-1009','بنفش یاسی',         '#7B1FA2'),
            ('SH-1010','فیروزه‌ای کاشان',  '#00838F'),
            ('SH-1011','خاکستری مات',       '#607D8B'),
            ('SH-1012','مشکی ذغالی',        '#212121'),
            ('SH-1013','قرمز گلی',          '#E53935'),
            ('SH-1014','آبی آسمانی',        '#1565C0'),
            ('SH-1015','سبز زیتونی',        '#33691E'),
            ('SH-1016','طلایی کهربا',       '#F57F17'),
            ('SH-1017','شتری گرم',          '#795548'),
            ('SH-1018','گلبهی ملایم',       '#F8BBD0'),
            ('SH-1019','سرمه‌ای تیره',      '#1A237E'),
            ('SH-1020','عنابی کاشان',       '#880E4F'),
        ]
        for code,name,hex_c in shades:
            if not ColorShade.objects.filter(code=code).exists():
                ColorShade.objects.create(
                    code=code, name=name, color_hex=hex_c,
                    is_approved=True, approved_by=approver,
                    approved_at=datetime.now()-timedelta(days=random.randint(10,120)))
        self.stdout.write(f'  ✓ {len(shades)} شید رنگ')

    # ── سفارشات — ۱۱۰ عدد در همه وضعیت‌ها ──────────────────────
    def _orders(self):
        from apps.orders.models import Order, Customer, ColorShade
        from apps.core.models import ProductionLine
        from apps.accounts.models import User

        customers = list(Customer.objects.all())
        shades    = list(ColorShade.objects.all())
        creator   = User.objects.filter(role='manager').first()
        today     = date.today()

        if not customers or not creator:
            return

        yarn_by_line = {
            'LINE-01': [
                ('نخ فرش اکریلیک ۱۰۰۰ دنیر/۲ لا','1000 دنیر/2',460000,560000),
                ('نخ فرش اکریلیک ۱۲۰۰ دنیر/۲ لا','1200 دنیر/2',510000,610000),
            ],
            'LINE-02': [
                ('نخ فرش اکریلیک ۸۰۰ دنیر/۲ لا','800 دنیر/2', 400000,490000),
                ('نخ فرش اکریلیک ۶۰۰ دنیر/۲ لا','600 دنیر/2', 370000,450000),
            ],
            'LINE-03': [
                ('نخ فرش پلی‌استر ۱۴۰۰ دنیر/۲ لا','1400 دنیر/2',330000,420000),
                ('نخ فرش پلی‌استر ۱۲۰۰ دنیر/۲ لا','1200 دنیر/2',310000,390000),
            ],
        }

        # 110 سفارش در همه وضعیت‌ها
        statuses = (
            ['draft']        * 10 +
            ['confirmed']    * 18 +
            ['in_production']* 28 +
            ['quality_check']* 14 +
            ['ready']        * 12 +
            ['delivered']    * 22 +
            ['cancelled']    *  6
        )
        random.shuffle(statuses)

        lines = list(ProductionLine.objects.all())
        n = 0
        for i, status in enumerate(statuses):
            order_date = today - timedelta(days=random.randint(0, 55))
            order_num  = f"ORD-{order_date.strftime('%Y%m%d')}-{i+1:04d}"
            if Order.objects.filter(order_number=order_num).exists():
                continue

            line = random.choice(lines)
            yarn_type, yarn_count, pmin, pmax = random.choice(
                yarn_by_line.get(line.code, yarn_by_line['LINE-01']))

            qty   = Decimal(str(random.randint(300, 5500)))
            price = Decimal(str(random.randint(pmin, pmax)))

            progress = {
                'draft': 0, 'confirmed': 0,
                'in_production': random.randint(10, 90),
                'quality_check':  random.randint(90, 98),
                'ready': 100, 'delivered': 100,
                'cancelled': random.randint(0, 60),
            }.get(status, 0)

            if status == 'delivered':
                delivery = order_date + timedelta(days=random.randint(15, 45))
            elif status == 'cancelled':
                delivery = order_date + timedelta(days=random.randint(20, 50))
            else:
                delivery = today + timedelta(days=random.randint(-8, 50))

            Order.objects.create(
                order_number=order_num,
                customer=random.choice(customers),
                color_shade=random.choice(shades) if shades else None,
                production_line=line,
                yarn_type=yarn_type, yarn_count=yarn_count,
                quantity_kg=qty, unit_price=price,
                total_price=qty * price,
                delivery_date=delivery,
                priority=random.choice(['low','normal','normal','normal','high','urgent']),
                status=status, progress_pct=progress,
                ply_count=2, heatset_required=True,
                process_sequence='no_dye',
                created_by=creator)
            n += 1

        self.stdout.write(f'  ✓ {n} سفارش')

    # ── نگهداری ──────────────────────────────────────────────────
    def _maintenance(self):
        from apps.maintenance.models import Schedule, WorkOrder, DowntimeLog
        from apps.core.models import Machine, Shift
        from apps.accounts.models import User

        machines = list(Machine.objects.all())
        techs    = list(User.objects.filter(department='maintenance'))
        op       = User.objects.filter(role='operator').first()
        shifts   = list(Shift.objects.all())
        if not machines or not op:
            return

        now_dt = datetime.now()
        for m in machines:
            tech = random.choice(techs) if techs else op
            Schedule.objects.get_or_create(
                machine=m, title=f'PM هفتگی {m.code}',
                defaults=dict(
                    maintenance_type='preventive', frequency='weekly',
                    description=f'تمیزکاری و روغن‌کاری {m.name}',
                    next_due_at=now_dt+timedelta(days=random.randint(-2,7)),
                    assigned_to=tech, priority='medium'))
            Schedule.objects.get_or_create(
                machine=m, title=f'PM ماهانه {m.code}',
                defaults=dict(
                    maintenance_type='preventive', frequency='monthly',
                    description=f'بازرسی کامل {m.name}',
                    next_due_at=now_dt+timedelta(days=random.randint(3,30)),
                    assigned_to=tech, priority='high'))
            if random.random() > 0.4:
                wo_num = f"WO-{date.today().strftime('%Y%m%d')}-{m.id:04d}"
                WorkOrder.objects.get_or_create(
                    wo_number=wo_num,
                    defaults=dict(
                        machine=m,
                        title=random.choice([
                            f'تعویض بلبرینگ {m.name}',
                            f'رفع نشتی روغن {m.name}',
                            f'تنظیم تسمه {m.name}',
                            f'سرویس موتور {m.name}',
                            f'کالیبراسیون {m.name}']),
                        wo_type=random.choice(['preventive','corrective','corrective']),
                        priority=random.choice(['low','medium','medium','high']),
                        status=random.choice(['open','open','in_progress','completed']),
                        reported_by=op, assigned_to=tech,
                        cost_parts=random.randint(0, 9_000_000),
                        cost_labor=random.randint(500_000, 3_500_000),
                        downtime_min=random.randint(30, 420)))
            for _ in range(random.randint(0, 3)):
                if shifts:
                    dur = random.randint(10, 180)
                    st  = datetime.now() - timedelta(hours=random.randint(2, 96))
                    DowntimeLog.objects.create(
                        machine=m, operator=op,
                        shift=random.choice(shifts),
                        start_time=st,
                        end_time=st + timedelta(minutes=dur),
                        duration_min=dur,
                        reason_category=random.choice([
                            'mechanical','mechanical','electrical',
                            'material','planned','operator']),
                        reason_detail=random.choice([
                            'گیر کردن نخ در مسیر','قطع برق موقت',
                            'تعویض شیطانک','سرویس روتین',
                            'کمبود مواد اولیه','پارگی تسمه',
                            'تنظیم تنش نخ','نمونه‌گیری کیفی']),
                        production_loss=Decimal(str(
                            round(random.uniform(5, 180), 2))))
        self.stdout.write('  ✓ نگهداری و توقفات')

    # ══════════════════════════════════════════════════════════════
    # HISTORICAL — N روز تاریخچه
    # ══════════════════════════════════════════════════════════════
    def _history(self, days=20):
        from apps.core.models import ProductionLine, Shift
        from apps.accounts.models import User
        from apps.orders.models import Order

        lines  = list(ProductionLine.objects.filter(status='active'))
        ops    = list(User.objects.filter(role='operator', is_active=True))
        orders = list(Order.objects.filter(
            status__in=['in_production','quality_check','ready','delivered']))
        today  = date.today()

        if not lines or not ops:
            return

        for offset in range(days, 0, -1):
            d = today - timedelta(days=offset)
            for line in lines:
                shifts = list(Shift.objects.filter(
                    production_line=line, is_active=True))
                if not shifts:
                    continue
                for shift in shifts:
                    op    = random.choice(ops)
                    order = random.choice(orders) if orders else None
                    for _ in range(random.randint(2, 4)):
                        self._b_blowroom(line, shift, op, order, d, hist=True)
                        self._b_carding( line, shift, op, order, d, hist=True)
                        self._b_passage( line, shift, op, order, d, hist=True)
                        self._b_finisher(line, shift, op, order, d, hist=True)
                        self._b_spinning(line, shift, op, order, d, hist=True)
                        self._b_winding( line, shift, op, order, d, hist=True)
                        self._b_tfo(     line, shift, op, order, d, hist=True)
                        self._b_heatset( line, shift, op, order, d, hist=True)
                    if random.random() > 0.72:
                        self._b_downtime(line, shift, op)

        self.stdout.write(f'  ✓ تاریخچه {days} روزه')

    # ══════════════════════════════════════════════════════════════
    # HOURLY — هر ساعت با cron
    # ══════════════════════════════════════════════════════════════
    def _hourly(self):
        from apps.core.models import ProductionLine
        from apps.accounts.models import User
        from apps.orders.models import Order

        lines  = list(ProductionLine.objects.filter(status='active'))
        ops    = list(User.objects.filter(role='operator', is_active=True))
        orders = list(Order.objects.filter(status='in_production'))
        today  = date.today()

        if not lines or not ops:
            self.stdout.write(self.style.WARNING('  داده پایه کم است. --reset اجرا کنید.'))
            return

        for line in lines:
            shift = self._cur_shift(line)
            if not shift:
                continue
            op    = random.choice(ops)
            order = random.choice(orders) if orders else None
            for _ in range(random.randint(1, 2)):
                self._b_blowroom(line, shift, op, order, today)
                self._b_carding( line, shift, op, order, today)
                self._b_passage( line, shift, op, order, today)
                self._b_finisher(line, shift, op, order, today)
                self._b_spinning(line, shift, op, order, today)
                self._b_winding( line, shift, op, order, today)
                self._b_tfo(     line, shift, op, order, today)
                self._b_heatset( line, shift, op, order, today)
            if random.random() > 0.65:
                self._b_downtime(line, shift, op)

        self.stdout.write('  ✓ بچ‌های ساعتی')

    # ══════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════
    def _cur_shift(self, line):
        from apps.core.models import Shift
        now = datetime.now().time()
        for s in Shift.objects.filter(production_line=line, is_active=True):
            st, et = s.start_time, s.end_time
            if st < et:
                if st <= now < et:
                    return s
            else:
                if now >= st or now < et:
                    return s
        return Shift.objects.filter(production_line=line).first()

    def _bn(self, prefix, d=None):
        d   = d or date.today()
        ts  = str(int(_tmod.time() * 1000))[-5:]
        rnd = random.randint(10, 99)
        return f"{prefix}-{d.strftime('%Y%m%d')}-{ts}{rnd}"

    def _ms(self, line, mtype):
        from apps.core.models import Machine
        return list(Machine.objects.filter(
            production_line=line, machine_type=mtype, status='active'))

    def _t0(self, d, hist=False):
        """زمان شروع بچ — سازگار با USE_TZ=False"""
        if hist and d:
            base = datetime.combine(d, datetime.min.time())
            return base + timedelta(hours=random.randint(0, 22),
                                    minutes=random.randint(0, 59))
        return datetime.now() - timedelta(hours=random.uniform(0.1, 2.5))

    def _ftype(self, line):
        ld = next((x for x in LINES if x['code'] == line.code), None)
        return ld['fiber'] if ld else 'acrylic'

    def _done(self, st, lo=0.8, hi=4.0, hist=False, sta=''):
        """زمان پایان بچ"""
        if sta == 'completed' or hist:
            return st + timedelta(hours=random.uniform(lo, hi))
        return None

    # ══════════════════════════════════════════════════════════════
    # BATCH CREATORS
    # ══════════════════════════════════════════════════════════════
    def _b_blowroom(self, line, shift, op, order, d, hist=False):
        from apps.blowroom.models import Batch, BatchInput
        from apps.inventory.models import FiberStock
        ms = self._ms(line, 'blowroom')
        if not ms:
            return
        m   = random.choice(ms)
        w_i = Decimal(str(round(random.uniform(250, 680), 2)))
        wpc = Decimal(str(round(random.uniform(1.5, 4.2), 2)))
        w_o = w_i * (1 - wpc / 100)
        st  = self._t0(d, hist)
        sta = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        ft  = self._ftype(line)
        b   = Batch.objects.create(
            batch_number=self._bn('BL', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            total_input_weight=w_i, output_weight=w_o,
            waste_weight=w_i - w_o, waste_pct=wpc,
            blend_recipe={'ACR': 100} if ft == 'acrylic' else {'PES': 100},
            started_at=st,
            completed_at=self._done(st, 1, 3.5, hist, sta))
        fibers = list(FiberStock.objects.filter(status='available', current_weight__gt=30))
        if fibers:
            BatchInput.objects.create(
                batch=b, fiber_stock=random.choice(fibers),
                weight_used=w_i, percentage=100)

    def _b_carding(self, line, shift, op, order, d, hist=False):
        from apps.carding.models import Production
        ms = self._ms(line, 'carding')
        if not ms:
            return
        m   = random.choice(ms)
        w_i = Decimal(str(round(random.uniform(170, 440), 2)))
        wpc = Decimal(str(round(random.uniform(3, 6.5), 2)))
        w_o = w_i * (1 - wpc / 100)
        st  = self._t0(d, hist)
        sta = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        Production.objects.create(
            batch_number=self._bn('CR', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            speed_rpm=Decimal(str(random.randint(280, 540))),
            sliver_count=Decimal('5.0'),
            sliver_weight_gperm=Decimal('5.0'),
            input_weight=w_i, output_weight=w_o,
            waste_weight=w_i - w_o, waste_pct=wpc,
            neps_count=random.randint(35, 230),
            started_at=st,
            completed_at=self._done(st, 1.5, 4.5, hist, sta))

    def _b_passage(self, line, shift, op, order, d, hist=False):
        from apps.passage.models import Production
        ms = self._ms(line, 'passage')
        if not ms:
            return
        m   = random.choice(ms)
        w_i = Decimal(str(round(random.uniform(120, 380), 2)))
        w_o = w_i * Decimal('0.97')
        st  = self._t0(d, hist)
        sta = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        Production.objects.create(
            batch_number=self._bn('PS', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            passage_number=random.choice([1, 2]),
            num_inputs=random.randint(6, 8),
            draft_ratio=Decimal(str(round(random.uniform(5.5, 8.5), 3))),
            output_sliver_count=Decimal('5.0'),
            input_total_weight=w_i, output_weight=w_o,
            speed_mpm=Decimal(str(round(random.uniform(280, 640), 1))),
            evenness_cv=Decimal(str(round(random.uniform(2.0, 5.2), 2))),
            started_at=st,
            completed_at=self._done(st, 0.8, 3, hist, sta))

    def _b_finisher(self, line, shift, op, order, d, hist=False):
        from apps.finisher.models import Production
        ms = self._ms(line, 'finisher')
        if not ms:
            return
        m   = random.choice(ms)
        w_i = Decimal(str(round(random.uniform(85, 290), 2)))
        w_o = w_i * Decimal('0.98')
        st  = self._t0(d, hist)
        sta = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        Production.objects.create(
            batch_number=self._bn('FN', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            draft_ratio=Decimal(str(round(random.uniform(6.0, 10.0), 3))),
            twist_tpm=Decimal(str(round(random.uniform(0.8, 1.6), 2))),
            output_sliver_count=Decimal('0.6'),
            speed_mpm=Decimal(str(round(random.uniform(13, 34), 1))),
            input_weight=w_i, output_weight=w_o,
            started_at=st,
            completed_at=self._done(st, 0.8, 2.5, hist, sta))

    def _b_spinning(self, line, shift, op, order, d, hist=False):
        from apps.spinning.models import Production
        ms = self._ms(line, 'ring')
        if not ms:
            return
        m   = random.choice(ms)
        w_o = Decimal(str(round(random.uniform(65, 235), 2)))
        ft  = self._ftype(line)
        tr  = (160, 260) if ft == 'acrylic' else (200, 330)
        sr  = (8500, 11500) if ft == 'acrylic' else (9000, 12500)
        st  = self._t0(d, hist)
        sta = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        Production.objects.create(
            batch_number=self._bn('RG', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            spindle_speed_rpm=random.randint(*sr),
            twist_tpm=Decimal(str(round(random.uniform(*tr), 1))),
            twist_direction=random.choice(['S', 'Z']),
            yarn_count=Decimal('14.50'),
            traveler_number=f'{random.randint(5,8)}/0 {random.choice(["SS","HO","EL"])}',
            input_weight=w_o * Decimal('1.02'), output_weight=w_o,
            num_spindles_active=random.randint(360, 480),
            num_spindles_total=480,
            breakage_count=random.randint(1, 32),
            efficiency_pct=Decimal(str(round(random.uniform(73, 97), 1))),
            started_at=st,
            completed_at=self._done(st, 1, 4, hist, sta))

    def _b_winding(self, line, shift, op, order, d, hist=False):
        from apps.winding.models import Production
        ms = self._ms(line, 'winding')
        if not ms:
            return
        m     = random.choice(ms)
        w_i   = Decimal(str(round(random.uniform(85, 300), 2)))
        waste = w_i * Decimal('0.015')
        w_o   = w_i - waste
        pkgs  = max(1, int(w_o / Decimal('2.5')))
        st    = self._t0(d, hist)
        sta   = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        Production.objects.create(
            batch_number=self._bn('WD', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            input_weight_kg=w_i, output_weight_kg=w_o,
            waste_weight_kg=waste,
            output_packages=pkgs,
            package_weight_kg=Decimal('2.5'),
            package_type='cone',
            winding_speed_mpm=Decimal(str(random.randint(900, 1900))),
            cuts_per_100km=random.randint(3, 42),
            splices_per_100km=random.randint(3, 42),
            efficiency_pct=Decimal(str(round(random.uniform(79, 97), 1))),
            started_at=st,
            completed_at=self._done(st, 0.8, 3, hist, sta))

    def _b_tfo(self, line, shift, op, order, d, hist=False):
        from apps.tfo.models import Production
        ms = self._ms(line, 'tfo')
        if not ms:
            return
        m   = random.choice(ms)
        w_i = Decimal(str(round(random.uniform(130, 400), 2)))
        w_o = w_i * Decimal('0.982')
        ft  = self._ftype(line)
        tr  = (180, 380) if ft == 'polyester' else (160, 320)
        st  = self._t0(d, hist)
        sta = 'completed' if hist else random.choice(['in_progress','completed','completed'])
        Production.objects.create(
            batch_number=self._bn('TF', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            ply_count=2,
            twist_tpm=Decimal(str(round(random.uniform(*tr), 1))),
            twist_direction=random.choice(['S', 'Z']),
            spindle_speed_rpm=random.randint(4500, 8800),
            tension_weight_g=Decimal(str(round(random.uniform(7, 22), 1))),
            input_packages=random.randint(50, 140),
            input_weight_kg=w_i,
            output_packages=random.randint(25, 70),
            output_weight_kg=w_o,
            waste_weight_kg=w_i - w_o,
            breakage_count=random.randint(0, 22),
            efficiency_pct=Decimal(str(round(random.uniform(77, 97), 1))),
            started_at=st,
            completed_at=self._done(st, 1, 3.5, hist, sta))

    def _b_heatset(self, line, shift, op, order, d, hist=False):
        from apps.heatset.models import Batch as HsB
        ms = self._ms(line, 'heatset')
        if not ms:
            return
        m   = random.choice(ms)
        ft  = self._ftype(line)
        tlo, thi = (132, 182) if ft == 'polyester' else (108, 138)
        wt   = Decimal(str(round(random.uniform(170, 440), 2)))
        pkgs = max(1, int(wt / Decimal('2.5')))
        dur  = random.randint(45, 105)
        st   = self._t0(d, hist)
        sta  = 'completed' if hist else random.choice(['processing','completed','completed'])
        done = sta == 'completed' or hist
        q    = (random.choices(['pass','pass','pass','conditional','fail'],
                               weights=[55,22,8,10,5])[0] if done else None)
        HsB.objects.create(
            batch_number=self._bn('HS', d),
            production_line=line, machine=m,
            operator=op, shift=shift, order=order,
            production_date=d, status=sta,
            machine_type_hs='superba',
            fiber_type=ft,
            cycle_type='standard',
            temperature_c=Decimal(str(round(random.uniform(tlo, thi), 1))),
            steam_pressure_bar=Decimal(str(round(random.uniform(1.1, 2.3), 2))),
            vacuum_level_mbar=Decimal(str(round(random.uniform(65, 165), 1))),
            pre_heat_min=random.randint(8, 16),
            vacuum_time_min=random.randint(6, 13),
            steam_time_min=random.randint(18, 48),
            dwell_time_min=random.randint(8, 26),
            cooldown_min=random.randint(12, 22),
            batch_weight_kg=wt, packages_count=pkgs,
            quality_result=q,
            shrinkage_pct=Decimal(str(round(random.uniform(0.3, 3.2), 2))),
            twist_stability=random.choices(
                ['excellent','good','good','fair','poor'],
                weights=[25,42,18,10,5])[0],
            started_at=st,
            completed_at=(st + timedelta(minutes=dur) if done else None))

    def _b_downtime(self, line, shift, op):
        from apps.maintenance.models import DowntimeLog
        from apps.core.models import Machine
        ms = list(Machine.objects.filter(production_line=line, status='active'))
        if not ms:
            return
        m   = random.choice(ms)
        dur = random.randint(8, 130)
        st  = datetime.now() - timedelta(minutes=dur + random.randint(0, 90))
        DowntimeLog.objects.create(
            machine=m, operator=op, shift=shift,
            production_line=line,
            start_time=st,
            end_time=st + timedelta(minutes=dur),
            duration_min=dur,
            reason_category=random.choice([
                'mechanical','mechanical','electrical',
                'material','planned','operator']),
            reason_detail=random.choice([
                'گیر کردن نخ در مسیر',
                'تعویض بوبین خالی',
                'تنظیم تنش نخ',
                'سرویس روتین شیفت',
                'کمبود مواد اولیه',
                'پارگی تسمه',
                'تعویض شیطانک',
                'نمونه‌گیری کیفی',
                'استراحت اپراتور',
                'انتقال مواد']),
            production_loss=Decimal(str(round(random.uniform(4, 140), 2))))
