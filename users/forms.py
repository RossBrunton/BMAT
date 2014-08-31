from django import forms
from django.contrib.auth.forms import UserCreationForm

class ImportForm(forms.Form):
    use_tags = forms.BooleanField(required=False)
    file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
