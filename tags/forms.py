from django import forms

from tags.models import Tag, colours_enum

class RenameTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["colour", "name"]


class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["colour", "name"]
    
    type = forms.CharField()
    pk = forms.IntegerField(min_value=1)


class RemoveTagForm(forms.Form):
    tag_pk = forms.IntegerField(min_value=1)
    type = forms.CharField()
    target_pk = forms.IntegerField(min_value=1)
