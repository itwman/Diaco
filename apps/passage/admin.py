from django.contrib import admin
from .models import Production, Input


class InputInline(admin.TabularInline):
    model = Input
    extra = 6
    fields = ('input_position', 'source_type', 'source_id', 'source_batch_number', 'weight_used')
    readonly_fields = ('created_at',)


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'passage_number', 'machine', 'num_inputs', 'draft_ratio', 'evenness_cv', 'status', 'production_date')
    list_filter = ('status', 'passage_number', 'production_date', 'machine')
    search_fields = ('batch_number',)
    list_per_page = 25
    date_hierarchy = 'production_date'
    raw_id_fields = ('machine', 'operator', 'order')
    inlines = [InputInline]
    readonly_fields = ('created_at', 'updated_at')
