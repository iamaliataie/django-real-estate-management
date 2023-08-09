from django.contrib import admin
from .models import Inquiry, InquiryReply

# Register your models here.

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    pass

@admin.register(InquiryReply)
class InquiryReplyAdmin(admin.ModelAdmin):
    pass