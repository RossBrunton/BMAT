""" Forms for manipulating tags """
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from bookmarks.models import Bookmark
from users.models import Settings

class RenameBookmarkForm(forms.ModelForm):
    """ A model form for renaming a bookmark
    
    It requires the fields "name" and "url".
    """
    class Meta:
        model = Bookmark
        fields = ["title", "url"]
    
    def __init__(self, user, *args, **kwargs):
        super(RenameBookmarkForm, self).__init__(*args, **kwargs)
        self.allow_invalid_urls = user.settings.url_settings != Settings.URL_SETTINGS_VALIDATE
    
    def clean_url(self):
        if self.allow_invalid_urls:
            return self.cleaned_data["url"]
        
        val = URLValidator()
        try:
            val(self.cleaned_data["url"])
        except ValidationError:
            try:
                val("http://"+self.cleaned_data["url"])
                self.cleaned_data["url"] = "http://"+self.cleaned_data["url"]
            except ValidationError:
                raise ValidationError("Invalid URL")
        
        return self.cleaned_data["url"]
