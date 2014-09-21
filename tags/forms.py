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
    
    def __init__(self, *args, **kwargs):
        kwargs["auto_id"] = False
        
        self.set_type = kwargs.get("taggable_type", "")
        
        kwargs.pop("taggable_type", None)
        super(AddTagForm, self).__init__(*args, **kwargs)


class RemoveTagForm(forms.Form):
    tag_pk = forms.IntegerField(min_value=1)
    type = forms.CharField()
    target_pk = forms.IntegerField(min_value=1)
    
    def __init__(self, *args, **kwargs):
        kwargs["auto_id"] = False
        
        self.set_type = kwargs.get("taggable_type", "")
        
        kwargs.pop("taggable_type", None)
        super(RemoveTagForm, self).__init__(*args, **kwargs)
