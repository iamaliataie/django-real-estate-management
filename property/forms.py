from django import forms
from django.forms import inlineformset_factory

from .models import (
    Property,
    Image,
)


class PropertyForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['features'].help_text = 'separate features using comma(,)'
        self.fields['latitude'].widget.attrs['readonly'] = True
        self.fields['longitude'].widget.attrs['readonly'] = True

    class Meta:
        model = Property
        exclude = ('agent',)

        widgets = {
            'features': forms.Textarea(attrs={'rows': 2, 'placeholder': 'eg: 1 floor, 2 bedrooms, 1 bathroom, 1 balcony, 1 parking, 2 parkings, basement'}),
            'description': forms.Textarea(attrs={'rows': 3, 'resize': 'none'}),
            'deal_date': forms.DateInput(attrs={'type': 'date'}),
        }


    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <0:
            raise forms.ValidationError('Price cannot be negative')
        return price


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']



ImageFormSet = inlineformset_factory(
    Property, Image, form=ImageForm,
    extra=1,
)