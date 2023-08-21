from django.contrib import admin
from .models import Property, Image, PropertyType

# Register your models here.


class ImageAdmin(admin.StackedInline):
    model = Image

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
       model = Property

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    pass
