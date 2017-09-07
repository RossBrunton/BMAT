""" Forms for manipulating tags """
from django import forms

from .models import Autotag

class AutotagSetPatternForm(forms.ModelForm):
    """ A model form for setting the pattern of an autotag rule
    
    It requires the fields "pattern".
    """
    class Meta:
        model = Autotag
        fields = ["pattern"]
