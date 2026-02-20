"""
Diaco MES - HeatSet Admin (هیت‌ست)
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Batch, CycleLog


class CycleLogInline(admin.TabularInline):
    model = CycleLog
    extra = 0
    readonly_fields = ['created_at']
    fields = ['log_time', 'elapsed_min', 'phase', 'temperature_c', 'pressure_bar', 'humidity_pct']
    can_delete = False


@admin.register(Batch)
class HeatSetBatchAdmin(admin.ModelAdmin):
    list_display = [
        'batch_number', 'production_date', 'machine',
        'fiber_type', 'temperature_c', 'batch_weight_kg',
        'quality_badge', 'twist_badge', 'status_badge',
    ]
    list_filter = ['status', 'quality_result', 'production_date', 'machine', 'fiber_type', 'machine_type_hs']
    search_fields = ['batch_number', 'machine__code']
    readonly_fields = ['created_at', 'updated_at', 'duration_min']
    date_hierarchy = 'production_date'
    inlines = [CycleLogInline]

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('batch_number', 'production_date', 'machine', 'operator', 'shift', 'order', 'production_line')
        }),
        ('ورودی از TFO', {
            'fields': ('tfo_production', 'batch_weight_kg', 'packages_count')
        }),
        ('مشخصات دستگاه', {
            'fields': ('machine_type_hs', 'fiber_type', 'cycle_type')
        }),
        ('پارامترهای حرارتی', {
            'fields': ('temperature_c', 'steam_pressure_bar', 'vacuum_level_mbar', 'humidity_pct')
        }),
        ('زمان‌بندی چرخه', {
            'fields': ('pre_heat_min', 'vacuum_time_min', 'steam_time_min', 'dwell_time_min', 'cooldown_min', 'duration_min'),
            'description': 'مدت کل به صورت خودکار محاسبه می‌شود',
        }),
        ('نتایج کیفی', {
            'fields': ('quality_result', 'shrinkage_pct', 'twist_stability')
        }),
        ('وضعیت', {
            'fields': ('status', 'started_at', 'completed_at', 'notes', 'metadata')
        }),
        ('سیستمی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def quality_badge(self, obj):
        if not obj.quality_result:
            return '-'
        colors = {'pass': '#28a745', 'fail': '#dc3545', 'conditional': '#ffc107'}
        labels = {'pass': 'قبول ✓', 'fail': 'رد ✗', 'conditional': 'مشروط'}
        color = colors.get(obj.quality_result, '#6c757d')
        label = labels.get(obj.quality_result, obj.quality_result)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:bold;">{}</span>',
            color, label
        )
    quality_badge.short_description = 'کیفیت'

    def twist_badge(self, obj):
        if not obj.twist_stability:
            return '-'
        colors = {'excellent': '#28a745', 'good': '#17a2b8', 'fair': '#ffc107', 'poor': '#dc3545'}
        labels = {'excellent': 'عالی', 'good': 'خوب', 'fair': 'متوسط', 'poor': 'ضعیف'}
        color = colors.get(obj.twist_stability, '#6c757d')
        label = labels.get(obj.twist_stability, obj.twist_stability)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{}</span>',
            color, label
        )
    twist_badge.short_description = 'پایداری تاب'

    def status_badge(self, obj):
        colors = {
            'loading': '#6c757d',
            'processing': '#17a2b8',
            'cooling': '#fd7e14',
            'completed': '#28a745',
            'failed': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'


@admin.register(CycleLog)
class CycleLogAdmin(admin.ModelAdmin):
    list_display = ['heatset_batch', 'log_time', 'phase', 'temperature_c', 'pressure_bar', 'humidity_pct']
    list_filter = ['phase', 'heatset_batch']
    readonly_fields = ['created_at']
