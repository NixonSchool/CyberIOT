from django import forms
from .models import Item, Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, Order
from django.utils import timezone

# TailwindCSS styling for input fields
INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class CreditCardForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'pattern': '\\d*',  # Corrected escape sequence for digits
            'maxlength': '16',
            'class': INPUT_CLASSES
        })
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'pattern': '(0[1-9]|1[0-2])\\/[0-9]{2}',  # Corrected escape sequence for date format
            'maxlength': '5',
            'placeholder': 'MM/YY',
            'class': INPUT_CLASSES
        })
    )
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'pattern': '\\d*',  # Corrected escape sequence for digits
            'maxlength': '3',
            'class': INPUT_CLASSES
        })
    )

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'monthly_price', 'image', 'quantity', 'status', 'available_from')
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'monthly_price': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Monthly price (for subscription items)'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
            'quantity': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': 0}),
            'status': forms.Select(attrs={'class': INPUT_CLASSES}),
            'available_from': forms.DateTimeInput(attrs={'class': INPUT_CLASSES, 'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        monthly_price = cleaned_data.get('monthly_price')

        if status == 'subscription' and not monthly_price:
            self.add_error('monthly_price', 'Monthly price is required for subscription items.')

        return cleaned_data


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'monthly_price', 'image', 'quantity', 'status', 'available_from')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'monthly_price': forms.TextInput(
                attrs={'class': INPUT_CLASSES, 'placeholder': 'Monthly price (for subscription items)'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
            'quantity': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': 0}),
            'status': forms.Select(attrs={'class': INPUT_CLASSES}),
            'available_from': forms.DateTimeInput(attrs={'class': INPUT_CLASSES, 'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        monthly_price = cleaned_data.get('monthly_price')

        if status == 'subscription' and not monthly_price:
            self.add_error('monthly_price', 'Monthly price is required for subscription items.')

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Write your comment here...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'min': 1,
                'max': 5,
            }),
        }
