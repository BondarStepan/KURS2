from django.forms import ModelForm
from django import forms
from dal import autocomplete
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
# Next two lines are only used for generating the upload preset sample name
from cloudinary.compat import to_bytes
import cloudinary, hashlib
from .models import compendium as comped


class CompendiumForm(ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    containment = forms.TextInput()

    class Meta:
        model = comped
        fields = {'name', 'containment'}


class TestForm(autocomplete.FutureModelForm):

    class Meta:
        model = comped
        fields = ('naming',)
        widgets = {
            'tags': autocomplete.TaggingSelect2(
                'country-autocomplete/'
            )
        }

