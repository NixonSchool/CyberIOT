from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Type your message here...',
                'rows': '4',
                'data-message-input': 'true',  # For potential JS enhancement
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''  # Remove label for cleaner UI