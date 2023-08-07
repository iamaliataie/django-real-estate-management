from django import forms
from django.forms import inlineformset_factory

from .models import (
    Property,
    Image,
)


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        exclude = ('agent',)


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']



ImageFormSet = inlineformset_factory(
    Property, Image, form=ImageForm,
    extra=1,
)