"""
Diaco MES - HeatSet Migration 0001 (هیت‌ست)
Migration: ساخت جداول heatset_batch و heatset_cyclelog

Generated: 1404-11-30
"""
import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_machine_type_v2_carpet_yarn'),
        ('orders', '0003_order_carpet_yarn_fields_v2'),
        ('tfo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('batch_number', models.CharField(max_length=50, unique=True, verbose_name='شماره بچ', help_text='HS-YYMMDD-NNN')),
                ('production_date', models.DateField(verbose_name='تاریخ تولید')),
                # ── نوع ماشین و فرآیند ──
                ('machine_type_hs', models.CharField(
                    choices=[
                        ('autoclave', 'اتوکلاو (Autoclave)'),
                        ('superba', 'سوپربا (Superba) - پیوسته'),
                        ('suessen', 'سوسن (Suessen) - حرارت خشک'),
                        ('other', 'سایر'),
                    ],
                    default='autoclave',
                    max_length=15,
                    verbose_name='نوع دستگاه هیت‌ست',
                )),
                ('fiber_type', models.CharField(
                    choices=[
                        ('polyester', 'پلی‌استر'),
                        ('acrylic', 'اکریلیک'),
                        ('wool', 'پشم'),
                        ('nylon', 'نایلون (PA)'),
                        ('polypropylene', 'پلی‌پروپیلن'),
                        ('blend', 'مخلوط'),
                    ],
                    default='polyester',
                    max_length=15,
                    verbose_name='نوع الیاف',
                )),
                ('cycle_type', models.CharField(
                    choices=[
                        ('standard', 'استاندارد'),
                        ('intensive', 'فشرده (Intensive)'),
                        ('gentle', 'ملایم (Gentle)'),
                    ],
                    default='standard',
                    max_length=15,
                    verbose_name='نوع چرخه',
                )),
                # ── پارامترهای حرارتی ──
                ('temperature_c', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='دمای تثبیت (°C)')),
                ('steam_pressure_bar', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True, verbose_name='فشار بخار (bar)')),
                ('vacuum_level_mbar', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='سطح خلأ (mbar)')),
                ('humidity_pct', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='رطوبت محفظه (%)')),
                # ── زمان‌بندی ──
                ('pre_heat_min', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='پیش‌گرم (دقیقه)')),
                ('vacuum_time_min', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='خلأ (دقیقه)')),
                ('steam_time_min', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='تزریق بخار (دقیقه)')),
                ('dwell_time_min', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='نگه‌داری (دقیقه)')),
                ('cooldown_min', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='سردشدن (دقیقه)')),
                ('duration_min', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='مدت کل (دقیقه)')),
                # ── بارگذاری ──
                ('batch_weight_kg', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='وزن بچ (kg)')),
                ('packages_count', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد بوبین')),
                # ── نتایج کیفی ──
                ('quality_result', models.CharField(
                    blank=True,
                    choices=[
                        ('pass', 'قبول ✓'),
                        ('fail', 'رد ✗'),
                        ('conditional', 'مشروط'),
                    ],
                    db_index=True,
                    max_length=15,
                    null=True,
                    verbose_name='نتیجه کیفی',
                )),
                ('shrinkage_pct', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='آنکاژ / کوچک‌شدن (%)')),
                ('twist_stability', models.CharField(
                    blank=True,
                    choices=[
                        ('excellent', 'عالی'),
                        ('good', 'خوب'),
                        ('fair', 'متوسط'),
                        ('poor', 'ضعیف'),
                    ],
                    max_length=15,
                    null=True,
                    verbose_name='پایداری تاب',
                )),
                # ── وضعیت ──
                ('status', models.CharField(
                    choices=[
                        ('loading', 'در حال بارگذاری'),
                        ('processing', 'در حال فرآیند'),
                        ('cooling', 'در حال سردشدن'),
                        ('completed', 'تکمیل شده'),
                        ('failed', 'ناموفق'),
                    ],
                    db_index=True,
                    default='loading',
                    max_length=15,
                    verbose_name='وضعیت',
                )),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='شروع')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='پایان')),
                ('notes', models.TextField(blank=True, default='', verbose_name='یادداشت')),
                ('metadata', models.JSONField(blank=True, default=dict, null=True, verbose_name='متادیتا (AI)')),
                # ── FKs ──
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='heatset_batches', to='core.machine', verbose_name='ماشین هیت‌ست')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='heatset_batches', to=settings.AUTH_USER_MODEL, verbose_name='اپراتور')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='heatset_batches', to='core.shift', verbose_name='شیفت')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='heatset_batches', to='orders.order', verbose_name='سفارش')),
                ('production_line', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='heatset_batches', to='core.productionline', verbose_name='خط تولید')),
                ('tfo_production', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='heatset_batches', to='tfo.production', verbose_name='بچ TFO ورودی')),
            ],
            options={
                'verbose_name': 'بچ هیت‌ست',
                'verbose_name_plural': 'بچ‌های هیت‌ست',
                'db_table': 'heatset_batch',
                'ordering': ['-production_date', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='batch',
            index=models.Index(fields=['production_date'], name='idx_hs_date'),
        ),
        migrations.AddIndex(
            model_name='batch',
            index=models.Index(fields=['machine'], name='idx_hs_machine'),
        ),
        migrations.AddIndex(
            model_name='batch',
            index=models.Index(fields=['status'], name='idx_hs_status'),
        ),
        migrations.AddIndex(
            model_name='batch',
            index=models.Index(fields=['quality_result'], name='idx_hs_quality'),
        ),
        migrations.AddIndex(
            model_name='batch',
            index=models.Index(fields=['order'], name='idx_hs_order'),
        ),
        # ────────────────────────────────────────────────────────────────
        # CycleLog — لاگ چرخه دما/فشار (AI-Ready)
        # ────────────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='CycleLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='زمان ثبت')),
                ('elapsed_min', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='دقیقه از شروع')),
                ('temperature_c', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='دمای لحظه‌ای (°C)')),
                ('pressure_bar', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True, verbose_name='فشار لحظه‌ای (bar)')),
                ('humidity_pct', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='رطوبت لحظه‌ای (%)')),
                ('phase', models.CharField(
                    choices=[
                        ('preheat', 'پیش‌گرم'),
                        ('vacuum', 'خلأ'),
                        ('steam', 'تزریق بخار'),
                        ('dwell', 'نگه‌داری'),
                        ('cooldown', 'سردشدن'),
                    ],
                    max_length=10,
                    verbose_name='مرحله فرآیند',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('heatset_batch', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='cycle_logs',
                    to='heatset.batch',
                    verbose_name='بچ هیت‌ست',
                )),
            ],
            options={
                'verbose_name': 'لاگ چرخه هیت‌ست',
                'verbose_name_plural': 'لاگ‌های چرخه هیت‌ست',
                'db_table': 'heatset_cyclelog',
                'ordering': ['heatset_batch', 'log_time'],
            },
        ),
        migrations.AddIndex(
            model_name='cyclelog',
            index=models.Index(fields=['heatset_batch'], name='idx_cl_batch'),
        ),
        migrations.AddIndex(
            model_name='cyclelog',
            index=models.Index(fields=['heatset_batch', 'log_time'], name='idx_cl_batch_time'),
        ),
    ]
