# forms.py
from django import forms

class ChangePasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)