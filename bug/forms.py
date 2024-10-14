from django import forms
from .models import Comment, Post
from django.utils.text import slugify
from django_summernote.widgets import SummernoteWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'privacy']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(attrs={'width': '100%', 'height': '400px'}),
            'privacy': forms.RadioSelect(attrs={'class': 'privacy-radio-group'}),
        }

        labels = {
            'privacy': 'Privacy',  # Custom label without asterisk
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            title = self.cleaned_data.get('title')
            slug = slugify(title)
        return slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['privacy'].widget.attrs['class'] = 'privacy-radio-group'
        self.fields['privacy'].initial = 'public'  # Set default to public

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            title = self.cleaned_data.get('title')
            slug = slugify(title)
        return slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
