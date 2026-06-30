from django import forms
from django.conf import settings
from .models import Car


class CarForm(forms.ModelForm):
    """Used by the dashboard to add and edit cars."""

    class Meta:
        model = Car
        fields = [
            'brand', 'car_name', 'model', 'price_per_day', 'fuel_type',
            'transmission', 'seats', 'mileage', 'description', 'image',
            'is_available',
        ]
        widgets = {
            'brand': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Maruti Suzuki'
            }),
            'car_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Swift'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 2023 VXi'
            }),
            'price_per_day': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 1500', 'step': '0.01', 'min': '0'
            }),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'seats': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '1', 'max': '20'
            }),
            'mileage': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 18 km/l'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Describe the car, its features and condition...'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Image file is too large. Maximum size is 5 MB.")
        return image

    def clean_price_per_day(self):
        price = self.cleaned_data.get('price_per_day')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price per day must be greater than zero.")
        return price
