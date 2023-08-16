from django.contrib import admin
from .models import Deal, DealType

# Register your models here.

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('property', 'deal_type', 'get_amount', 'get_total_days', 'get_total',)

@admin.register(DealType)
class DealTypeAdmin(admin.ModelAdmin):
    pass