from django import forms
from django.conf import settings
from django.utils import timezone

from .models import Booking


class BookingForm(forms.ModelForm):
    """Public booking form filled by customers (no account required)."""

    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone_number', 'email', 'driving_license',
            'pickup_date', 'pickup_time', 'return_date', 'return_time',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your full name', 'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '10-digit phone number',
                'maxlength': '15', 'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'your.email@example.com (optional)',
            }),
            'driving_license': forms.ClearableFileInput(attrs={
                'class': 'form-control', 'accept': 'image/*,.pdf', 'required': True,
            }),
            'pickup_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date', 'required': True,
            }),
            'pickup_time': forms.TimeInput(attrs={
                'class': 'form-control', 'type': 'time', 'required': True,
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date', 'required': True,
            }),
            'return_time': forms.TimeInput(attrs={
                'class': 'form-control', 'type': 'time', 'required': True,
            }),
        }

    def __init__(self, *args, car=None, **kwargs):
        self.car = car
        super().__init__(*args, **kwargs)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid phone number (at least 10 digits).")
        return phone

    def clean_driving_license(self):
        license_file = self.cleaned_data.get('driving_license')
        if license_file and hasattr(license_file, 'size'):
            if license_file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Driving license file is too large. Maximum size is 5 MB.")
        return license_file

    def clean_pickup_date(self):
        pickup_date = self.cleaned_data.get('pickup_date')
        if pickup_date and pickup_date < timezone.localdate():
            raise forms.ValidationError("Pickup date cannot be in the past.")
        return pickup_date

    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        pickup_time = cleaned_data.get('pickup_time')
        return_date = cleaned_data.get('return_date')
        return_time = cleaned_data.get('return_time')

        if pickup_date and pickup_time and return_date and return_time:
            from datetime import datetime
            pickup_dt = datetime.combine(pickup_date, pickup_time)
            return_dt = datetime.combine(return_date, return_time)

            if return_dt <= pickup_dt:
                raise forms.ValidationError(
                    "Return date and time must be after the pickup date and time."
                )

            # Check for double booking against the selected car
            if self.car is not None:
                active_statuses = [Booking.STATUS_PENDING, Booking.STATUS_APPROVED]
                conflicting = Booking.objects.filter(
                    car=self.car,
                    status__in=active_statuses,
                )
                if self.instance and self.instance.pk:
                    conflicting = conflicting.exclude(pk=self.instance.pk)

                for existing in conflicting:
                    existing_pickup_dt = datetime.combine(existing.pickup_date, existing.pickup_time)
                    existing_return_dt = datetime.combine(existing.return_date, existing.return_time)
                    if existing_pickup_dt < return_dt and pickup_dt < existing_return_dt:
                        raise forms.ValidationError(
                            "This car is already booked for an overlapping time period. "
                            "Please choose different dates or select another car."
                        )

        return cleaned_data


class BookingSearchForm(forms.Form):
    """Used by customers to search for their bookings using their phone number."""

    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your registered phone number',
        }),
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid phone number (at least 10 digits).")
        return phone
