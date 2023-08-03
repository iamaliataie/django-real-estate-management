from django import forms
from django.core.validators import RegexValidator

from .models import Inquiry

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
    
    email = Lowercase(
        label="Email Address",
        max_length=100,
        validators=[
                RegexValidator(
                    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',
                    message='Enter a valid email address'
                    )
                ],
        widget=forms.TextInput(attrs={'placeholder': 'Email Address'})
    )
    
    content = forms.CharField(
        label="Message",
        max_length=255,
        widget=forms.Textarea(attrs={'placeholder': 'Your message','rows': 3, 'style': 'resize:none'})
    )
    
    class Meta:
        model = Inquiry
        exclude = ('property', 'created_at',)
    
        widgets = {
        "phone": forms.TextInput(
            attrs={
                'placeholder': 'e.g +93 XXXXXXXXX',
                'data-mask': '(+00) 000-000-0000'
                }
            ),
        }