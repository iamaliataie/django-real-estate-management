from django import forms
from django.forms import inlineformset_factory

from .models import (
    Property,
    Image,
)


class PropertyForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['features'].help_text = 'Hold down “Control”, or “Command” on a Mac, to select more than one.'
        self.fields['latitude'].widget.attrs['readonly'] = True
        self.fields['longitude'].widget.attrs['readonly'] = True

    class Meta:
        model = Property
        exclude = ('agent',)

        widgets = {
            'features': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3, 'resize': 'none'}),
        }
        
class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image']



ImageFormSet = inlineformset_factory(
    Property, Image, form=ImageForm,
    extra=1,
)