"""
Diaco MES - Winding Admin (بوبین‌پیچی)
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Production


@admin.register(Production)
class WindingProductionAdmin(admin.ModelAdmin):
    list_display = [
        'batch_number', 'production_date', 'machine',
        'input_cops', 'output_packages', 'package_type',
        'cuts_badge', 'efficiency_badge', 'status_badge',
    ]
    list_filter = ['status', 'production_date', 'machine', 'package_type']
    search_fields = ['batch_number', 'machine__code']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'production_date'

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('batch_number', 'production_date', 'machine', 'operator', 'shift', 'order', 'production_line')
        }),
        ('ورودی از رینگ', {
            'fields': ('spinning_production', 'input_cops', 'input_weight_kg')
        }),
        ('تنظیمات ماشین', {
            'fields': ('winding_speed_mpm', 'tension_setting_cn', 'yarn_clearer_type')
        }),
        ('بوبین‌های خروجی', {
            'fields': ('package_type', 'package_weight_kg', 'output_packages', 'output_weight_kg', 'waste_weight_kg')
        }),
        ('شاخص‌های کیفیت', {
            'fields': ('cuts_per_100km', 'splices_per_100km', 'efficiency_pct'),
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

    def cuts_badge(self, obj):
        if obj.cuts_per_100km is None:
            return '-'
        c = obj.cuts_per_100km
        if c < 20:
            color = '#28a745'
        elif c < 40:
            color = '#17a2b8'
        elif c < 60:
            color = '#ffc107'
        else:
            color = '#dc3545'
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{}</span>',
            color, f'{c} برش'
        )
    cuts_badge.short_description = 'کیفیت (Cuts)'

    def efficiency_badge(self, obj):
        if obj.efficiency_pct is None:
            return '-'
        e = float(obj.efficiency_pct)
        color = '#28a745' if e >= 85 else ('#ffc107' if e >= 70 else '#dc3545')
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
