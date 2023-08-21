from django.db import models
from account.models import User

from property.models import Property, PropertyType

# Create your models here.

class SearchCriteria(models.Model):
    type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING, null=True, blank=True)
    city = models.CharField(max_length=50, default='', null=True, blank=True)
    price_from = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    price_to = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Search Criteria'
    
    def __str__(self):
        return self.type.title