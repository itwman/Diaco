"""
Diaco MES - Orders Migration 0003
Migration: اضافه کردن فیلدهای نخ فرش به Order (v2.0)
  - ply_count: تعداد لا
  - heatset_required: نیاز به هیت‌ست
  - process_sequence: ترتیب فرآیند رنگرزی

Generated: 1404-11-30
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_production_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ply_count',
            field=models.PositiveSmallIntegerField(
                default=1,
                help_text='۱=تک‌لا، ۲=دولا (معمولاً برای نخ فرش)',
                verbose_name='تعداد لا',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='heatset_required',
            field=models.BooleanField(
                default=False,
                help_text='آیا نخ باید هیت‌ست شود؟',
                verbose_name='نیاز به هیت‌ست',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='process_sequence',
            field=models.CharField(
                choices=[
                    ('no_dye', 'بدون رنگرزی'),
                    ('pre_dye', 'رنگرزی قبل از هیت‌ست'),
                    ('post_dye', 'رنگرزی بعد از هیت‌ست'),
                    ('stock_dye', 'رنگرزی الیاف (Stock Dyeing)'),
                ],
                default='no_dye',
                help_text='آیا رنگرزی قبل، بعد یا بدون هیت‌ست انجام شود؟',
                max_length=20,
                verbose_name='ترتیب فرآیند',
            ),
        ),
    ]
