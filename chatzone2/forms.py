from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Search users...'}))
