from django import forms

from .models import Customer

class FileUploadedForm(forms.Form):
    uploaded_file = forms.FileField(required=False)


class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['id']
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Name'}),
            'contract' : forms.TextInput(attrs={'class':'form-control','placeholder': 'E-Tag Number'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control','placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
