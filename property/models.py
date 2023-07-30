import os
from django.db import models

# Create your models here.


def path_generator(instance, filename):
    
    return f'{instance}/{filename}'

class Property(models.Model):
    type = models.ForeignKey('PropertyType', on_delete=models.DO_NOTHING, related_name='properties')
    owner = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __str__(self) -> str:
        return self.owner


class Image(models.Model):
    property= models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True
        , related_name='images')
    image = models.ImageField(blank=True, upload_to=path_generator)

    def __str__(self):
        return self.property.owner


class PropertyType(models.Model):
    title = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'
    
    
    def __str__(self) -> str:
        return self.title
    
    
