from django import forms

from tags.models import Tag, colours_enum

class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["colour", "name"]
    
