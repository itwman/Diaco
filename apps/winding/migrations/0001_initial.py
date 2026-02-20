"""
Diaco MES - Winding Migration 0001 (بوبین‌پیچی)
Migration: ساخت جدول winding_production

Generated: 1404-11-30
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_machine_type_v2_carpet_yarn'),
        ('orders', '0003_order_carpet_yarn_fields_v2'),
        ('spinning', '0002_production_production_line'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('batch_number', models.CharField(max_length=50, unique=True, verbose_name='شماره بچ')),
                ('production_date', models.DateField(verbose_name='تاریخ تولید')),
                ('status', models.CharField(
                    choices=[
                        ('in_progress', 'در حال تولید'),
                        ('completed', 'تکمیل شده'),
                        ('quality_hold', 'توقف کیفی'),
                        ('cancelled', 'لغو شده'),
                    ],
                    db_index=True,
                    default='in_progress',
                    max_length=20,
                    verbose_name='وضعیت',
                )),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='شروع')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='پایان')),
                ('notes', models.TextField(blank=True, default='', verbose_name='یادداشت')),
                ('metadata', models.JSONField(blank=True, default=dict, null=True, verbose_name='متادیتا (AI)')),
                # ── ورودی از رینگ ──
                ('input_cops', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد بوبین ورودی (Cop)')),
                ('input_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='وزن ورودی (kg)')),
                # ── پارامترهای ماشین ──
                ('winding_speed_mpm', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='سرعت بوبین‌پیچی (m/min)')),
                ('tension_setting_cn', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='تنظیم کشش (cN)')),
                ('yarn_clearer_type', models.CharField(blank=True, default='', max_length=100, verbose_name='نوع Yarn Clearer')),
                # ── بوبین‌های خروجی ──
                ('package_type', models.CharField(
                    choices=[('cone', 'کُن (Cone)'), ('cheese', 'چیز (Cheese)'), ('spool', 'اسپول (Spool)')],
                    default='cone',
                    max_length=10,
                    verbose_name='نوع بوبین خروجی',
                )),
                ('package_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='وزن هر بوبین خروجی (kg)')),
                ('output_packages', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد بوبین خروجی')),
                ('output_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='وزن خروجی کل (kg)')),
                ('waste_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='ضایعات (kg)')),
                # ── کیفیت (AI) ──
                ('cuts_per_100km', models.PositiveIntegerField(blank=True, null=True, verbose_name='برش در ۱۰۰ کیلومتر')),
                ('splices_per_100km', models.PositiveIntegerField(blank=True, null=True, verbose_name='اتصال در ۱۰۰ کیلومتر')),
                ('efficiency_pct', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='راندمان (%)')),
                # ── FKs ──
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='winding_production_set', to='core.machine', verbose_name='ماشین')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='winding_production_set', to=settings.AUTH_USER_MODEL, verbose_name='اپراتور')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='winding_production_set', to='core.shift', verbose_name='شیفت')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winding_production_set', to='orders.order', verbose_name='سفارش')),
                ('production_line', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='winding_production_set', to='core.productionline', verbose_name='خط تولید')),
                ('spinning_production', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winding_productions', to='spinning.production', verbose_name='بچ رینگ ورودی')),
            ],
            options={
                'verbose_name': 'تولید بوبین‌پیچی',
                'verbose_name_plural': 'تولیدات بوبین‌پیچی',
                'db_table': 'winding_production',
                'ordering': ['-production_date', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['production_date'], name='idx_wd_date'),
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['machine'], name='idx_wd_machine'),
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['status'], name='idx_wd_status'),
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['order'], name='idx_wd_order'),
        ),
    ]
