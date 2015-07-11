""" Forms for user management """
from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Settings

class ImportForm(forms.Form):
    """ The form used to import a bookmark file """
    use_tags = forms.BooleanField(required=False)
    file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    """ Subclass of the normal UserCreationForm to add an optional email """
    email = forms.EmailField(required=False)

class SettingsForm(forms.ModelForm):
    """ And a form to edit settings, specifically the theme """
    class Meta:
        model = Settings
        fields = ("theme", "url_settings", "no_analytics")
