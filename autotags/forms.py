""" Forms for manipulating tags """
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import Autotag
from users.models import Settings

class AutotagSetPatternForm(forms.ModelForm):
    """ A model form for setting the pattern of an autotag rule
    
    It requires the fields "pattern".
    """
    class Meta:
        model = Autotag
        fields = ["pattern"]
