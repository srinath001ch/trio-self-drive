from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Public contact form used on the Contact Us page."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'phone_number', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit phone number',
                'maxlength': '15',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com (optional)',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
                'rows': 5,
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid phone number (at least 10 digits).")
        return phone
