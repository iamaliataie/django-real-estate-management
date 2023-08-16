from django.db import models
from property.models import Property

# Create your models here.

class Deal(models.Model):
    deal_type = models.ForeignKey('DealType', on_delete=models.DO_NOTHING, related_name='deals', null=True)
    agent = models.ForeignKey('account.User', on_delete=models.DO_NOTHING, null=True, related_name='agent_deals')
    property = models.ForeignKey(Property, on_delete=models.DO_NOTHING, related_name='property_deals')
    owner = models.CharField(max_length=50)
    tazkira = models.CharField(max_length=50)
    address = models.TextField()
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
    
    def __str__(self):
        return self.property.title
    

class DealType(models.Model):
    title = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Deal Type'
        verbose_name_plural = 'Deal Types'
    
    def __str__(self):
        return self.title