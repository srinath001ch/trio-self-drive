from django.db import models
from django.urls import reverse


class Car(models.Model):
    """Represents a self-drive rental car listed by Trio Self Drive."""

    FUEL_PETROL = 'petrol'
    FUEL_DIESEL = 'diesel'
    FUEL_ELECTRIC = 'electric'
    FUEL_CNG = 'cng'
    FUEL_HYBRID = 'hybrid'

    FUEL_TYPE_CHOICES = [
        (FUEL_PETROL, 'Petrol'),
        (FUEL_DIESEL, 'Diesel'),
        (FUEL_ELECTRIC, 'Electric'),
        (FUEL_CNG, 'CNG'),
        (FUEL_HYBRID, 'Hybrid'),
    ]

    TRANSMISSION_MANUAL = 'manual'
    TRANSMISSION_AUTOMATIC = 'automatic'

    TRANSMISSION_CHOICES = [
        (TRANSMISSION_MANUAL, 'Manual'),
        (TRANSMISSION_AUTOMATIC, 'Automatic'),
    ]

    brand = models.CharField(max_length=80, help_text="e.g. Maruti Suzuki, Hyundai, Toyota")
    car_name = models.CharField(max_length=100, help_text="e.g. Swift, Creta, Innova Crysta")
    model = models.CharField(max_length=50, help_text="e.g. 2023, VXi, ZX")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default=FUEL_PETROL)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default=TRANSMISSION_MANUAL)
    seats = models.PositiveSmallIntegerField(default=5)
    mileage = models.CharField(max_length=50, help_text="e.g. 18 km/l or 220 km/charge")
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')
    is_available = models.BooleanField(default=True, help_text="Uncheck to hide this car from bookings.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f"{self.brand} {self.car_name} ({self.model})"

    def get_absolute_url(self):
        return reverse('cars:car_detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f"{self.brand} {self.car_name} {self.model}"
