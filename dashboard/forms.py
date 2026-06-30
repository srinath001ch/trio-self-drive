from django import forms
from django.contrib.auth.forms import AuthenticationForm


class DashboardLoginForm(AuthenticationForm):
    """Styled login form for the staff dashboard."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
        })
    )


class BookingDecisionForm(forms.Form):
    """Used by staff to approve/reject a booking with an optional note."""

    admin_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional note (e.g. reason for rejection)...',
        }),
    )
