from django.contrib import admin
from .models import SearchCriteria

# Register your models here.

@admin.register(SearchCriteria)
class SearchCriteriaAdmin(admin.ModelAdmin):
    pass