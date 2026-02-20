"""
Diaco MES - TFO Migration 0001 (دولاتابی)
Migration: ساخت جدول tfo_production

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
        ('winding', '0001_initial'),
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
                # ── مشخصات نخ ──
                ('ply_count', models.PositiveSmallIntegerField(default=2, verbose_name='تعداد لا')),
                ('input_yarn_count_ne', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='نمره نخ ورودی (Ne)')),
                ('output_yarn_count_ne', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='نمره نخ خروجی (Ne)')),
                # ── پارامترهای تاب ──
                ('twist_tpm', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='تاب (TPM)')),
                ('twist_direction', models.CharField(
                    choices=[('S', 'S (چپ‌تاب)'), ('Z', 'Z (راست‌تاب)')],
                    default='S',
                    max_length=1,
                    verbose_name='جهت تاب',
                )),
                ('spindle_speed_rpm', models.PositiveIntegerField(blank=True, null=True, verbose_name='سرعت دوک (RPM)')),
                ('tension_weight_g', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='وزن تانسیون (g)')),
                ('balloon_control', models.BooleanField(default=False, verbose_name='کنترل بالون')),
                # ── تولید ──
                ('input_packages', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد بوبین ورودی')),
                ('input_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='وزن ورودی (kg)')),
                ('output_packages', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد بوبین خروجی')),
                ('output_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='وزن خروجی (kg)')),
                ('waste_weight_kg', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='ضایعات (kg)')),
                # ── کیفیت (AI) ──
                ('breakage_count', models.PositiveIntegerField(default=0, verbose_name='تعداد پارگی')),
                ('efficiency_pct', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='راندمان (%)')),
                # ── FKs ──
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tfo_production_set', to='core.machine', verbose_name='ماشین')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tfo_production_set', to=settings.AUTH_USER_MODEL, verbose_name='اپراتور')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tfo_production_set', to='core.shift', verbose_name='شیفت')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tfo_production_set', to='orders.order', verbose_name='سفارش')),
                ('production_line', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tfo_production_set', to='core.productionline', verbose_name='خط تولید')),
                ('winding_production', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tfo_productions', to='winding.production', verbose_name='بچ بوبین‌پیچی ورودی')),
            ],
            options={
                'verbose_name': 'تولید دولاتابی TFO',
                'verbose_name_plural': 'تولیدات دولاتابی TFO',
                'db_table': 'tfo_production',
                'ordering': ['-production_date', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['production_date'], name='idx_tfo_date'),
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['machine'], name='idx_tfo_machine'),
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['status'], name='idx_tfo_status'),
        ),
        migrations.AddIndex(
            model_name='production',
            index=models.Index(fields=['order'], name='idx_tfo_order'),
        ),
    ]
