""" Forms for user management """
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Settings

class ThemeSelect(forms.widgets.ChoiceWidget):
    input_type = "input"
    template_name = "users/forms/themeSelect.html"
    option_template_name = "users/forms/themeSelectOption.html"
    checked_attribute = {"data-selected": True}
    option_inherits_attrs = False

class ImportForm(forms.Form):
    """ The form used to import a bookmark file """
    use_tags = forms.BooleanField(required=False)
    file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    """ Subclass of the normal UserCreationForm to add an optional email """
    email = forms.EmailField(required=False)

class SettingsForm(forms.ModelForm):
    """ And a form to edit settings """
    class Meta:
        model = Settings
        fields = ("url_settings", "no_analytics", "hide_settings")

class ThemeForm(forms.ModelForm):
    """ And a form to edit theme settings """
    class Meta:
        model = Settings
        fields = ("theme",)
    
    theme = forms.ChoiceField(choices=Settings.THEME_OPTIONS, widget=ThemeSelect)

class EmailForm(forms.ModelForm):
    """ And a form to edit settings, specifically the theme """
    class Meta:
        model = User
        fields = ("email",)
