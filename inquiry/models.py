from django.db import models
from property.models import Property

# Create your models here.

INQUIRIES = (
    ('information', 'Information'),
    ('sales', 'About Sales'),
    ('payment', 'About Payment'),
    ('schedule', 'About Schedule'),
)

STATUS = (
    ('read', 'Read'),
    ('unread', 'unread'),
)


class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    type = models.CharField('Topic', max_length=50, choices=INQUIRIES)
    status = models.CharField('Status', max_length=6, choices=STATUS, blank=True, null=True, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
        
    def __str__(self) -> str:
        return self.title
    
    def type_color(self):
        if self.type == 'information':
            return 'primary'
        elif self.type == 'sales':
            return 'success'
        elif self.type == 'payment':
            return 'danger'
        return 'warning'


class InquiryReply(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='replies')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inquiry reply'
        verbose_name_plural = 'Inquiry replies'
        
    def __str__(self):
        return self.inquiry.title