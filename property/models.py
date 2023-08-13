from django.contrib.postgres.fields import ArrayField
from django.db import models
# Create your models here.


def path_generator(instance, filename):
    
    return f'{instance}/{filename}'

class Property(models.Model):
    type = models.ForeignKey('PropertyType', on_delete=models.DO_NOTHING, related_name='properties')
    owner = models.CharField(max_length=50)
    agent = models.ForeignKey('account.User', on_delete=models.DO_NOTHING, null=True, related_name='agent_properties')
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    size = models.CharField(max_length=50)
    # colors = ArrayField(models.CharField(max_length=10, blank=True), size=2, default=list)
    description = models.TextField()
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __str__(self) -> str:
        return self.title

    
    def get_type_colors(self):
        if self.type == 'Commercial':
            return 'red', 'danger'
        return 'yellow', 'warning'
    
    

class Image(models.Model):
    property= models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True
        , related_name='images')
    image = models.ImageField(blank=True, upload_to=path_generator)

    def __str__(self):
        return self.property.title


class PropertyType(models.Model):
    title = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'
    
    
    def __str__(self) -> str:
        return self.title
    
    
