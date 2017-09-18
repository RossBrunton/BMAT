""" Forms for manipulating tags """
from django import forms

from tags.models import Tag, colours_enum

class ColourSelect(forms.widgets.ChoiceWidget):
    input_type = "input"
    template_name = "tags/forms/colourSelect.html"
    option_template_name = "tags/forms/colourSelectOption.html"
    checked_attribute = {"data-selected": True}
    option_inherits_attrs = False

class RenameTagForm(forms.ModelForm):
    """ A model form for renaming a tag
    
    It requires the fields "colour" and "name".
    """
    class Meta:
        model = Tag
        fields = ["colour", "name"]
    
    colour = forms.ChoiceField(choices=colours_enum, widget=ColourSelect)

class PinTagForm(forms.ModelForm):
    """ A model form for pinning and unpinning a tag
    
    It requires the "pinned" field.
    """
    class Meta:
        model = Tag
        fields = ["pinned"]


class AddTagForm(forms.ModelForm):
    """ A model form for adding a new tag
    
    It requires the fields "colour" and "name". It also has additional fields "type" and "pk", which are the type and
    primary key of the thing to be tagged as well.
    """
    class Meta:
        model = Tag
        fields = ["colour", "name"]
    
    def __init__(self, *args, **kwargs):
        super(AddTagForm, self).__init__(*args, **kwargs)
        
        self.type_str = args[0].get("type")
    
    type = forms.CharField()
    pk = forms.IntegerField(min_value=1)
    colour = forms.ChoiceField(choices=colours_enum, widget=ColourSelect)


class RemoveTagForm(forms.Form):
    """ A form for removing a tag
    
    It requires the fields "tag_pk", "type" and "target_pk". "type" and "target_pk" describe the thing that will be
    untagged, while "tag_pk" is the primary key of the tag to untag.
    """
    tag_pk = forms.IntegerField(min_value=1)
    type = forms.CharField()
    target_pk = forms.IntegerField(min_value=1)
