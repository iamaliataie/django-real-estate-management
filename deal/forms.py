from django import forms
from .models import Deal
from property.models import Property

class DealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['agent'].initial = user
        self.fields['agent'].widget.attrs['readonly'] = 'readonly'
        if user.is_superuser:
            self.fields['property'] = forms.ModelChoiceField(queryset = Property.objects.filter(active=True, deal=False))
        else:
            self.fields['property'] = forms.ModelChoiceField(queryset = Property.objects.filter(agent=user).filter(active=True, deal=False))
        
        
    class Meta:
        model = Deal
        exclude = ('created_at',)
        
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'style': 'resize:none; white-space: pre-line'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }