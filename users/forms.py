from django import forms

class ImportForm(forms.Form):
    use_tags = forms.BooleanField(required=False)
    file = forms.FileField()
