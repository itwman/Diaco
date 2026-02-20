"""
Diaco MES - TFO Admin (دولاتابی)
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Production


@admin.register(Production)
class TFOProductionAdmin(admin.ModelAdmin):
    list_display = [
        'batch_number', 'production_date', 'machine',
        'ply_count', 'twist_tpm', 'twist_direction',
        'breakage_count', 'efficiency_badge', 'status_badge',
    ]
    list_filter = ['status', 'production_date', 'machine', 'twist_direction', 'ply_count']
    search_fields = ['batch_number', 'machine__code']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'production_date'

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('batch_number', 'production_date', 'machine', 'operator', 'shift', 'order', 'production_line')
        }),
        ('ورودی از بوبین‌پیچی', {
            'fields': ('winding_production', 'input_packages', 'input_weight_kg')
        }),
        ('مشخصات نخ', {
            'fields': ('ply_count', 'input_yarn_count_ne', 'output_yarn_count_ne')
        }),
        ('پارامترهای تاب', {
            'fields': ('twist_tpm', 'twist_direction', 'spindle_speed_rpm', 'tension_weight_g', 'balloon_control')
        }),
        ('تولید و خروجی', {
            'fields': ('output_packages', 'output_weight_kg', 'waste_weight_kg')
        }),
        ('کیفیت و راندمان', {
            'fields': ('breakage_count', 'efficiency_pct'),
            'classes': ('collapse',),
        }),
        ('وضعیت', {
            'fields': ('status', 'started_at', 'completed_at', 'notes', 'metadata')
        }),
        ('سیستمی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def efficiency_badge(self, obj):
        if obj.efficiency_pct is None:
            return '-'
        e = float(obj.efficiency_pct)
        color = '#28a745' if e >= 90 else ('#ffc107' if e >= 75 else '#dc3545')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{}</span>',
            color, f'{e:.1f}%'
        )
    efficiency_badge.short_description = 'راندمان'

    def status_badge(self, obj):
        colors = {
            'in_progress': '#17a2b8',
            'completed': '#28a745',
            'quality_hold': '#ffc107',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'
