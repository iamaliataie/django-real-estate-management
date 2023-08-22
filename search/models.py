from django.db import models
from account.models import User
from property.models import Property, PropertyType

# Create your models here.

class SearchCriteria(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True, default='')
    price_from = models.CharField(max_length=20, null=True, blank=True, default='')
    price_to = models.CharField(max_length=20, null=True, blank=True, default='')
    floors = models.CharField(max_length=20, null=True, blank=True, default='')
    bedrooms = models.CharField(max_length=20, null=True, blank=True, default='')
    bathrooms = models.CharField(max_length=20, null=True, blank=True, default='')
    parking = models.CharField(max_length=20, null=True, blank=True, default='')
    basement = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Search Criteria'
    
    def __str__(self):
        return self.user.get_full_name()
    
    
    def get_search_criteria(self):
        criteria = list()
        for key, value in self.__dict__.items():
            if key == 'user_id' or key == 'id' or key == '_state':
                continue
            
            if key == 'type_id':
                type = PropertyType.objects.filter(pk=value).first()
                key = 'type'
                if type:
                    value = type.title
            
            if value is None:
                value = ''
            
            if key == 'basement':
                value = 'Yes' if value else 'No'
            
            criteria.append((key, value))
        return criteria