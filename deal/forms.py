from django import forms
from .models import Deal
from property.models import Property

class DealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        
    class Meta:
        model = Deal
        exclude = ('created_at',)
        
        widgets = {
            'agent': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows': 3, 'style': 'resize:none; white-space: pre-line'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }