from django import forms

class FileUploadedForm(forms.Form):
    uploaded_file = forms.FileField(required=False)
