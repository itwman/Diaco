"""
Diaco MES - سیستم شماره‌گذاری یکپارچه بچ (تاریخ شمسی)
=========================================================

استاندارد شماره‌گذاری:
    [پیشوند]-[YYMMDD شمسی]-[NNN]

مثال‌ها:
    BL-040929-001   ← بچ حلاجی (BLowroom)، ۲۹ آذر ۱۴۰۴
    CR-040929-001   ← بچ کاردینگ (CaRding)
    PS-040929-003   ← بچ پاساژ (PaSsage)، سومین بچ روز
    FN-040929-001   ← بچ فینیشر (FiNisher)
    SP-040929-001   ← بچ ریسندگی (SPinning) — رینگ
    DY-040929-001   ← بچ رنگرزی (DYeing)
    PES-040929-001  ← ورود الیاف پلی‌استر
    ACR-040929-001  ← ورود الیاف اکریلیک
    WOL-040929-001  ← ورود الیاف پشم
    FB-040929-001   ← ورود الیاف عمومی (FiBer)
    ORD-040929-001  ← شماره سفارش (ORDer)
    WO-040929-001   ← دستور کار تعمیر (Work Order)

چرا شمسی؟
    - افراد با تاریخ میلادی آشنایی کمتری دارند
    - خواندن و تطبیق تاریخ در کارخانه آسان‌تر است
    - ردیابی بچ‌ها با تاریخ روزانه سریع‌تر می‌شود
    - مثال: «بچ CR-040929» یعنی کارد ۲۹ آذر ۱۴۰۴ ✓
"""

from jdatetime import date as jdate


# ══════════════════════════════════════════════════════════════
# نگاشت پیشوند به پیشوند الیاف (بر اساس کد دسته)
# ══════════════════════════════════════════════════════════════

# کد دسته الیاف → پیشوند بچ
FIBER_PREFIX_MAP = {
    'PES': 'PES',   # پلی‌استر
    'ACR': 'ACR',   # اکریلیک
    'WOL': 'WOL',   # پشم
    'VIS': 'VIS',   # ویسکوز
    'NYL': 'NYL',   # نایلون
    'COT': 'COT',   # پنبه
}

# پیشوندهای ثابت مراحل تولید
PRODUCTION_PREFIXES = {
    'blowroom':  'BL',
    'carding':   'CR',
    'passage':   'PS',
    'finisher':  'FN',
    'spinning':  'SP',
    # ── v2.0: خط تولید نخ فرش ──────────────────────
    'winding':   'WD',
    'tfo':       'TFO',
    'heatset':   'HS',
    # ────────────────────────────────────────────────
    'dyeing':    'DY',
    'order':     'ORD',
    'workorder': 'WO',
    'fiber':     'FB',   # الیاف عمومی (اگر دسته ناشناخته)
}


def _jalali_today_short() -> str:
    """تاریخ شمسی امروز به فرمت YYMMDD (بدون قرن)"""
    j = jdate.today()
    # سال دو رقمی: ۱۴۰۴ → ۰۴
    yy = str(j.year)[2:]
    mm = f"{j.month:02d}"
    dd = f"{j.day:02d}"
    return f"{yy}{mm}{dd}"


def jalali_today_full() -> str:
    """تاریخ شمسی امروز به فرمت YYYYMMDD (با قرن) — برای نمایش"""
    j = jdate.today()
    return f"{j.year}{j.month:02d}{j.day:02d}"


def jalali_today_display() -> str:
    """تاریخ شمسی برای نمایش: ۱۴۰۴/۰۹/۲۹"""
    j = jdate.today()
    return f"{j.year}/{j.month:02d}/{j.day:02d}"


def next_batch_number(prefix: str, model_or_queryset) -> str:
    """
    شماره بچ بعدی را بر اساس تاریخ شمسی امروز تولید می‌کند.

    آرگومان‌ها:
        prefix: پیشوند بچ (مثال: 'BL', 'CR', 'PES')
        model_or_queryset: مدل Django یا queryset که فیلد batch_number دارد

    خروجی:
        رشته شماره بچ — مثال: 'BL-040929-001'
    """
    date_part = _jalali_today_short()
    pattern = f"{prefix}-{date_part}-"

    # اگر queryset بود مستقیم استفاده کن، اگر model بود all() بگیر
    try:
        qs = model_or_queryset.objects.filter(
            batch_number__startswith=pattern
        ).order_by('-batch_number').first()
    except AttributeError:
        qs = model_or_queryset.filter(
            batch_number__startswith=pattern
        ).order_by('-batch_number').first()

    n = 1
    if qs:
        try:
            n = int(qs.batch_number.split('-')[-1]) + 1
        except (ValueError, IndexError):
            pass

    return f"{pattern}{n:03d}"


def next_order_number() -> str:
    """
    شماره سفارش بعدی: ORD-YYMMDD-NNN (شمسی)
    مثال: ORD-040929-007

    نکته: مدل Order فیلد order_number دارد نه batch_number
    پس مستقیماً قرى یکتا را حساب می‌کنیم
    """
    from apps.orders.models import Order
    date_part = _jalali_today_short()
    pattern = f"ORD-{date_part}-"
    last = Order.objects.filter(
        order_number__startswith=pattern
    ).order_by('-order_number').first()
    n = 1
    if last:
        try:
            n = int(last.order_number.split('-')[-1]) + 1
        except (ValueError, IndexError):
            pass
    return f"{pattern}{n:03d}"


def next_workorder_number(downtime_pk: int = None) -> str:
    """
    شماره دستور کار: WO-YYMMDD-NNN (شمسی)
    مثال: WO-040929-003
    """
    from apps.maintenance.models import WorkOrder
    date_part = _jalali_today_short()
    pattern = f"WO-{date_part}-"
    last = WorkOrder.objects.filter(
        wo_number__startswith=pattern
    ).order_by('-wo_number').first()
    n = 1
    if last:
        try:
            n = int(last.wo_number.split('-')[-1]) + 1
        except (ValueError, IndexError):
            pass
    return f"{pattern}{n:03d}"


def fiber_prefix_from_category(category_code: str) -> str:
    """
    پیشوند بچ الیاف بر اساس کد دسته.
    مثال: 'PES' → 'PES', 'XYZ' → 'FB'
    """
    return FIBER_PREFIX_MAP.get(category_code.upper(), 'FB')


def next_fiber_batch(category_code: str) -> str:
    """
    شماره بچ الیاف با پیشوند هوشمند بر اساس نوع الیاف.
    مثال: پلی‌استر → 'PES-040929-001'
    """
    from apps.inventory.models import FiberStock
    prefix = fiber_prefix_from_category(category_code)
    return next_batch_number(prefix, FiberStock)
