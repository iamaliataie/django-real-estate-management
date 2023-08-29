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
            'amount': forms.TextInput(attrs={'type': 'number', 'min': 1, 'id':'numberInput'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if end_date < start_date:
            raise forms.ValidationError('End date cannot be before start date')
        return end_date
    