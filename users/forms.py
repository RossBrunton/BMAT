from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Settings

class ImportForm(forms.Form):
    use_tags = forms.BooleanField(required=False)
    file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ("theme",)
