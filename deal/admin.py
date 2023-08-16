from django.contrib import admin
from .models import Deal, DealType

# Register your models here.

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass

@admin.register(DealType)
class DealTypeAdmin(admin.ModelAdmin):
    pass