"""
Diaco MES - Orders Admin
===========================
پنل مدیریت سفارشات، مشتریان و شید رنگی.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, ColorShade, ColorApprovalHistory, Order


# ═══════════════════════════════════════════════════════════════
# CUSTOMER
# ═══════════════════════════════════════════════════════════════

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'city', 'mobile', 'credit_limit', 'is_active')
    list_filter = ('is_active', 'province')
    search_fields = ('name', 'company', 'phone', 'mobile', 'tax_id')
    list_per_page = 25


# ═══════════════════════════════════════════════════════════════
# COLOR SHADE
# ═══════════════════════════════════════════════════════════════

class ColorApprovalInline(admin.TabularInline):
    model = ColorApprovalHistory
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('customer', 'status', 'sample_image', 'customer_feedback', 'reviewed_by', 'created_at')


@admin.register(ColorShade)
class ColorShadeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'color_preview_display', 'approval_badge', 'approved_by', 'approved_at')
    list_filter = ('is_approved',)
    search_fields = ('code', 'name')
    list_per_page = 25
    inlines = [ColorApprovalInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('اطلاعات رنگ', {
            'fields': ('code', 'name', 'color_hex', 'image'),
        }),
        ('فرمول', {
            'fields': ('recipe',),
        }),
        ('تأیید', {
            'fields': ('is_approved', 'approved_by', 'approved_at'),
        }),
        ('سایر', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def color_preview_display(self, obj):
        if obj.color_hex:
            return format_html(
                '<span style="display:inline-block; width:24px; height:24px; '
                'background:{}; border:1px solid #ccc; border-radius:4px; '
                'vertical-align:middle;"></span> {}',
                obj.color_hex, obj.color_hex
            )
        return '-'
    color_preview_display.short_description = 'رنگ'

    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="background:#198754; color:#fff; padding:2px 8px; '
                'border-radius:4px; font-size:11px;">✓ تأیید شده</span>'
            )
        return format_html(
            '<span style="background:#dc3545; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">○ در انتظار</span>'
        )
    approval_badge.short_description = 'وضعیت تأیید'


# ═══════════════════════════════════════════════════════════════
# ORDER
# ═══════════════════════════════════════════════════════════════

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'customer', 'yarn_type', 'quantity_kg',
        'priority_badge', 'status_badge', 'progress_bar', 'delivery_date',
    )
    list_filter = ('status', 'priority', 'delivery_date')
    search_fields = ('order_number', 'customer__name', 'yarn_type')
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('customer', 'color_shade', 'created_by')

    fieldsets = (
        ('شناسه', {
            'fields': ('order_number', 'customer', 'created_by'),
        }),
        ('مشخصات نخ', {
            'fields': ('color_shade', 'yarn_type', 'yarn_count', 'quantity_kg'),
        }),
        ('مالی', {
            'fields': ('unit_price', 'total_price'),
        }),
        ('زمان‌بندی و وضعیت', {
            'fields': ('delivery_date', 'priority', 'status', 'progress_pct'),
        }),
        ('سایر', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def priority_badge(self, obj):
        colors = {
            'low': '#6c757d', 'normal': '#0d6efd',
            'high': '#fd7e14', 'urgent': '#dc3545',
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = 'اولویت'

    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d', 'confirmed': '#0d6efd',
            'in_production': '#fd7e14', 'quality_check': '#6f42c1',
            'ready': '#20c997', 'delivered': '#198754',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'

    def progress_bar(self, obj):
        pct = obj.progress_pct
        color = '#198754' if pct >= 80 else '#fd7e14' if pct >= 40 else '#dc3545'
        return format_html(
            '<div style="width:80px; background:#e9ecef; border-radius:4px; overflow:hidden;">'
            '<div style="width:{}%; background:{}; height:18px; line-height:18px; '
            'color:#fff; text-align:center; font-size:11px;">{}%</div></div>',
            pct, color, pct
        )
    progress_bar.short_description = 'پیشرفت'
