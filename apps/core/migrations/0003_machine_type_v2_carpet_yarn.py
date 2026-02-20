"""
Diaco MES - Core Migration 0003
Migration: اضافه کردن winding, tfo, heatset به نوع‌های ماشین (v2.0)

Generated: 1404-11-30
"""
import django.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_shift_code_productionline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='machine_type',
            field=models.CharField(
                choices=[
                    ('blowroom', 'حلاجی'),
                    ('carding', 'کاردینگ'),
                    ('passage', 'پاساژ / کشش'),
                    ('finisher', 'فینیشر'),
                    ('ring', 'رینگ'),
                    ('winding', 'بوبین‌پیچی'),
                    ('tfo', 'دولاتابی (TFO)'),
                    ('heatset', 'هیت‌ست'),
                    ('dyeing', 'دستگاه رنگرزی'),
                    ('boiler', 'دیگ بخار'),
                    ('dryer', 'خشک‌کن'),
                ],
                db_index=True,
                max_length=20,
                verbose_name='نوع ماشین',
            ),
        ),
    ]
