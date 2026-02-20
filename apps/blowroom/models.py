"""
Diaco MES - Blowroom Models (حلاجی)
======================================
اولین مرحله تولید: باز کردن، تمیز کردن و مخلوط‌سازی الیاف خام.

منطق صنعتی:
───────────
Batch (بچ حلاجی):
  هر بچ حلاجی از ترکیب چند بسته الیاف (از انبار) تشکیل می‌شود.
  فرمول مخلوط (blend_recipe) نسبت هر نوع الیاف را مشخص می‌کند.
  مثال: ۷۰% پلی‌استر + ۳۰% ویسکوز
  خروجی: الیاف باز و تمیز شده آماده کاردینگ.

BatchInput (ورودی بچ):
  هر سطر یک بسته الیاف از انبار است که در بچ مصرف شده.
  weight_used از current_weight انبار کسر می‌شود.
  percentage سهم هر الیاف در مخلوط نهایی.
"""
from django.db import models
from apps.core.models import ProductionBaseModel
from apps.inventory.models import FiberStock


class Batch(ProductionBaseModel):
    """بچ حلاجی - اولین مرحله تولید."""

    # ── وزن ──────────────────────────────────────────────
    total_input_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        verbose_name='وزن کل ورودی (kg)',
    )
    output_weight = models.DecimalField(
        max_digits=12, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن خروجی (kg)',
    )
    waste_weight = models.DecimalField(
        max_digits=10, decimal_places=3,
        blank=True, null=True,
        verbose_name='وزن ضایعات (kg)',
    )
    waste_pct = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='درصد ضایعات',
    )

    # ── فرمول مخلوط ─────────────────────────────────────
    blend_recipe = models.JSONField(
        blank=True, null=True, default=dict,
        verbose_name='فرمول مخلوط',
        help_text='نسبت الیاف: {"PES": 70, "VIS": 30}',
    )

    class Meta:
        db_table = 'blowroom_batch'
        verbose_name = 'بچ حلاجی'
        verbose_name_plural = 'بچ‌های حلاجی'
        indexes = [
            models.Index(fields=['production_date'], name='idx_bl_date'),
        ]

    @property
    def calculated_waste_pct(self):
        if self.total_input_weight and self.output_weight:
            waste = self.total_input_weight - self.output_weight
            return round((waste / self.total_input_weight) * 100, 2)
        return None


class BatchInput(models.Model):
    """ورودی‌های بچ حلاجی - الیاف مصرفی از انبار."""

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        verbose_name='بچ',
        related_name='inputs',
    )
    fiber_stock = models.ForeignKey(
        FiberStock,
        on_delete=models.PROTECT,
        verbose_name='الیاف انبار',
        related_name='blowroom_usages',
    )
    weight_used = models.DecimalField(
        max_digits=12, decimal_places=3,
        verbose_name='وزن مصرفی (kg)',
    )
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='درصد در مخلوط',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت',
    )

    class Meta:
        db_table = 'blowroom_batchinput'
        verbose_name = 'ورودی بچ حلاجی'
        verbose_name_plural = 'ورودی‌های بچ حلاجی'

    def __str__(self):
        return f"{self.batch.batch_number} ← {self.fiber_stock.batch_number} ({self.weight_used}kg)"
