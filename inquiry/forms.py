from django import forms
from django.core.validators import RegexValidator

from .models import Inquiry, InquiryReply

class Capitalize(forms.CharField):
    def to_python(self, value):
        return value.capitalize()

class Lowercase(forms.CharField):
    def to_python(self, value):
        return value.lower()


class InquiryForm(forms.ModelForm):
    
    title = forms.CharField(
        label="Title",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Title'})
    )
    
    name = Capitalize(
        max_length=100,
        validators=[
                RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', message='Only letters are allowed'),
                ],
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    
    email = Lowercase(
        label="Email Address",
        max_length=100,
        validators=[
                RegexValidator(
                    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',
                    message='Enter a valid email address'
                    )
                ],
        widget=forms.TextInput(attrs={'placeholder': 'We reply to your email address'})
    )
    
    content = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'placeholder': 'Your message','rows': 3, 'style': 'resize:none; white-space: pre-line'}),
    )
    
    class Meta:
        model = Inquiry
        exclude = ('property', 'created_at',)
    
        widgets = {
        "phone": forms.TextInput(
            attrs={
                'placeholder': 'e.g +93 XXXXXXXXX',
                'data-mask': '(+00) 000-000-0000',
                }
            ),
        }
        
        
class InquiryReplyForm(forms.ModelForm):
    
    content = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'placeholder': 'Your message','rows': 3, 'style': 'resize:none'})
    )
    
    class Meta:
        model = InquiryReply
        fields = ('subject', 'content')