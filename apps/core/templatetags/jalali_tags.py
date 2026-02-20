"""
Diaco MES - فیلترهای تاریخ شمسی
=================================
تبدیل خودکار تاریخ‌های میلادی به شمسی در تمپلیت‌ها.

استفاده:
    {% load jalali_tags %}
    {{ my_date|to_jalali }}           →  ۱۴۰۴/۱۱/۲۸
    {{ my_datetime|to_jalali_dt }}    →  ۱۴۰۴/۱۱/۲۸ ۱۳:۴۵
    {{ my_date|to_jalali_long }}      →  ۲۸ بهمن ۱۴۰۴
    {{ my_date|to_jalali_relative }} →  ۲ روز پیش
"""
import jdatetime
from datetime import date, datetime
from django import template
from django.utils import timezone

register = template.Library()


def _to_jdate(value):
    """تبدیل date/datetime میلادی به jdatetime.date شمسی."""
    if value is None:
        return None
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return jdatetime.date.fromgregorian(date=value.date())
    if isinstance(value, date):
        return jdatetime.date.fromgregorian(date=value)
    # اگر رشته باشه تلاش برای پارس
    try:
        d = datetime.fromisoformat(str(value))
        return jdatetime.date.fromgregorian(date=d.date())
    except (ValueError, TypeError):
        return None


def _to_jdatetime(value):
    """تبدیل datetime میلادی به jdatetime.datetime شمسی."""
    if value is None:
        return None
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return jdatetime.datetime.fromgregorian(datetime=value)
    if isinstance(value, date):
        return jdatetime.datetime.fromgregorian(
            datetime=datetime.combine(value, datetime.min.time())
        )
    try:
        d = datetime.fromisoformat(str(value))
        return jdatetime.datetime.fromgregorian(datetime=d)
    except (ValueError, TypeError):
        return None


# ───────────────────────────────────────────────────────────
# فیلترهای اصلی
# ───────────────────────────────────────────────────────────

@register.filter(name='to_jalali')
def to_jalali(value):
    """
    تبدیل تاریخ میلادی به شمسی: ۱۴۰۴/۱۱/۲۸
    """
    jd = _to_jdate(value)
    if jd is None:
        return value or '-'
    return jd.strftime('%Y/%m/%d')


@register.filter(name='to_jalali_dt')
def to_jalali_dt(value):
    """
    تبدیل تاریخ+ساعت به شمسی: ۱۴۰۴/۱۱/۲۸ ۱۳:۴۵
    """
    jdt = _to_jdatetime(value)
    if jdt is None:
        return value or '-'
    return jdt.strftime('%Y/%m/%d %H:%M')


@register.filter(name='to_jalali_long')
def to_jalali_long(value):
    """
    تبدیل تاریخ به فرم بلند: ۲۸ بهمن ۱۴۰۴
    """
    jd = _to_jdate(value)
    if jd is None:
        return value or '-'
    months = [
        '', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
    ]
    return f'{jd.day} {months[jd.month]} {jd.year}'


@register.filter(name='to_jalali_short')
def to_jalali_short(value):
    """
    تبدیل تاریخ بدون سال: ۲۸ بهمن
    """
    jd = _to_jdate(value)
    if jd is None:
        return value or '-'
    months = [
        '', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
    ]
    return f'{jd.day} {months[jd.month]}'


@register.filter(name='to_jalali_relative')
def to_jalali_relative(value):
    """
    نمایش نسبی: امروز، دیروز، ۳ روز پیش، ۲ هفته پیش
    """
    jd = _to_jdate(value)
    if jd is None:
        return value or '-'
    today = jdatetime.date.today()
    delta = (today - jd).days

    if delta == 0:
        return 'امروز'
    elif delta == 1:
        return 'دیروز'
    elif delta == -1:
        return 'فردا'
    elif 2 <= delta <= 6:
        return f'{delta} روز پیش'
    elif -6 <= delta <= -2:
        return f'{abs(delta)} روز بعد'
    elif 7 <= delta <= 13:
        return 'هفته پیش'
    elif 14 <= delta <= 29:
        w = delta // 7
        return f'{w} هفته پیش'
    elif delta >= 30:
        m = delta // 30
        return f'{m} ماه پیش'
    elif delta <= -7:
        return jd.strftime('%Y/%m/%d')
    return jd.strftime('%Y/%m/%d')
