from django import forms
from django.contrib.auth.models import User

from tags.models import Tag, colours_enum

import re

class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["colour", "name"]
    
