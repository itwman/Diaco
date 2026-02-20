"""
Diaco MES - Inventory Admin
==============================
پنل مدیریت انبار مواد اولیه.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import FiberCategory, FiberStock, DyeStock, ChemicalStock, StockTransaction


# ═══════════════════════════════════════════════════════════════
# FIBER CATEGORY
# ═══════════════════════════════════════════════════════════════

@admin.register(FiberCategory)
class FiberCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name', 'code')
    list_per_page = 20


# ═══════════════════════════════════════════════════════════════
# FIBER STOCK
# ═══════════════════════════════════════════════════════════════

@admin.register(FiberStock)
class FiberStockAdmin(admin.ModelAdmin):
    list_display = (
        'batch_number', 'category', 'supplier', 'quality_badge',
        'weight_display', 'status', 'received_date',
    )
    list_filter = ('status', 'quality_grade', 'category', 'received_date')
    search_fields = ('batch_number', 'lot_number', 'supplier')
    list_per_page = 25
    date_hierarchy = 'received_date'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('شناسه بچ', {
            'fields': ('category', 'batch_number', 'lot_number'),
        }),
        ('تأمین‌کننده', {
            'fields': ('supplier', 'color_raw'),
        }),
        ('مشخصات فنی', {
            'fields': ('denier', 'staple_length'),
        }),
        ('وزن و مالی', {
            'fields': ('initial_weight', 'current_weight', 'unit_price'),
        }),
        ('انبارداری', {
            'fields': ('received_date', 'expiry_date', 'warehouse_loc', 'status', 'quality_grade'),
        }),
        ('سایر', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def quality_badge(self, obj):
        colors = {'A': '#198754', 'B': '#fd7e14', 'C': '#dc3545'}
        color = colors.get(obj.quality_grade, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">درجه {}</span>',
            color, obj.quality_grade
        )
    quality_badge.short_description = 'کیفیت'

    def weight_display(self, obj):
        pct = obj.consumed_pct
        color = '#198754' if pct < 50 else '#fd7e14' if pct < 80 else '#dc3545'
        return format_html(
            '{} / {} kg <span style="color:{};">({}% مصرف)</span>',
            obj.current_weight, obj.initial_weight, color, int(pct)
        )
    weight_display.short_description = 'وزن (فعلی/اولیه)'


# ═══════════════════════════════════════════════════════════════
# DYE STOCK
# ═══════════════════════════════════════════════════════════════

@admin.register(DyeStock)
class DyeStockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'dye_type', 'current_weight', 'unit', 'status', 'received_date')
    list_filter = ('dye_type', 'status', 'color_family')
    search_fields = ('code', 'name', 'manufacturer', 'batch_number')
    list_per_page = 25
    date_hierarchy = 'received_date'
    readonly_fields = ('created_at', 'updated_at')


# ═══════════════════════════════════════════════════════════════
# CHEMICAL STOCK
# ═══════════════════════════════════════════════════════════════

@admin.register(ChemicalStock)
class ChemicalStockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'chemical_type', 'current_amount', 'unit', 'concentration', 'status', 'received_date')
    list_filter = ('chemical_type', 'status')
    search_fields = ('code', 'name', 'manufacturer', 'batch_number')
    list_per_page = 25
    date_hierarchy = 'received_date'
    readonly_fields = ('created_at', 'updated_at')


# ═══════════════════════════════════════════════════════════════
# STOCK TRANSACTION
# ═══════════════════════════════════════════════════════════════

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'transaction_type', 'stock_type', 'stock_id', 'quantity', 'unit', 'performed_by')
    list_filter = ('transaction_type', 'stock_type', 'created_at')
    search_fields = ('reference_type', 'notes')
    list_per_page = 50
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
