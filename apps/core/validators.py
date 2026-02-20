"""
Diaco MES - Core Validators
==============================
ولیدیتورهای مشترک بین ماژول‌ها.
"""
import re
from django.core.exceptions import ValidationError


def validate_national_code(value):
    """
    اعتبارسنجی کد ملی ایرانی (۱۰ رقمی).
    الگوریتم رسمی بررسی کد ملی.
    """
    if not value:
        return

    if not re.match(r'^\d{10}$', value):
        raise ValidationError('کد ملی باید ۱۰ رقم باشد.')

    # بررسی تکراری نبودن همه ارقام
    if len(set(value)) == 1:
        raise ValidationError('کد ملی نامعتبر است.')

    # الگوریتم بررسی
    check = int(value[9])
    total = sum(int(value[i]) * (10 - i) for i in range(9))
    remainder = total % 11

    if remainder < 2:
        if check != remainder:
            raise ValidationError('کد ملی نامعتبر است.')
    else:
        if check != 11 - remainder:
            raise ValidationError('کد ملی نامعتبر است.')


def validate_machine_code(value):
    """
    اعتبارسنجی کد ماشین.
    فرمت: XX-NN (دو حرف - عدد)
    مثال: CR-01, RG-15, BL-02
    """
    if not re.match(r'^[A-Z]{2}-\d{1,3}$', value):
        raise ValidationError(
            'کد ماشین باید به فرمت XX-NN باشد. مثال: CR-01, RG-15'
        )
