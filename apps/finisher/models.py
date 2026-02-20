"""
Diaco MES - Finisher Models (فینیشر)
======================================
مرحله چهارم: کشش نهایی و تاب اولیه فتیله قبل از رینگ.

منطق صنعتی:
───────────
Production (تولید فینیشر):
  ورودی: فتیله از پاساژ دوم.
  خروجی: فتیله نازک‌تر با تاب اولیه، آماده رینگ.
  twist_tpm: تاب اولیه (دور بر متر) - فقط فینیشر و رینگ تاب دارند.
"""
from django.db import models
from apps.core.models import ProductionBaseModel


class Production(ProductionBaseModel):
    """تولید فینیشر - کشش نهایی و تاب اولیه."""

    # ── ارتباط با پاساژ ─────────────────────────────────
    passage_production = models.ForeignKey(
        'passage.Production',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='بچ پاساژ',
        related_name='finisher_productions',
    )

    # ── پارامترهای فنی ──────────────────────────────────
    draft_ratio = models.DecimalField(
        max_digits=8, decimal_places=3,
        blank=True, null=True,
        verbose_name='نسبت کشش نهایی',
    )
    twist_tpm = models.DecimalField(
        max_digits=8, decimal_places=2,
        blank=True, null=True,
        verbose_name='تاب اولیه (TPM)',
        help_text='دور بر متر',
    )
    output_sliver_count = models.DecimalField(
        max_digits=8, decimal_places=3,
        verbose_name='نمره فتیله خروجی',
    )
    speed_mpm = models.DecimalField(
        max_digits=8, decimal_places=2,
        blank=True, null=True,
        verbose_name='سرعت (m/min)',
    )

    # ── وزن ──────────────────────────────────────────────
    input_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن ورودی (kg)',
    )
    output_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن خروجی (kg)',
    )

    class Meta:
        db_table = 'finisher_production'
        verbose_name = 'تولید فینیشر'
        verbose_name_plural = 'تولیدات فینیشر'
        indexes = [
            models.Index(fields=['production_date'], name='idx_fn_date'),
        ]
