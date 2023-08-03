from django.db import models
from property.models import Property

# Create your models here.

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
        
    
    def __str__(self) -> str:
        return self.title
    