from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'))
