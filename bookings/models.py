from datetime import datetime, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from cars.models import Car


def license_upload_path(instance, filename):
    """Store driving licenses under media/licenses/<booking-temp>/filename."""
    return f"licenses/{filename}"


class Booking(models.Model):
    """A self-drive car booking made by a (non-registered) customer."""

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')

    # Customer details (no account / registration required)
    customer_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(blank=True, null=True)
    driving_license = models.ImageField(upload_to=license_upload_path)

    # Rental period
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    return_date = models.DateField()
    return_time = models.TimeField()

    # Auto-calculated
    total_days = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    admin_note = models.TextField(blank=True, null=True, help_text="Internal note, e.g. reason for rejection.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.customer_name} - {self.car} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('bookings:booking_status', kwargs={'pk': self.pk})

    @property
    def pickup_datetime(self):
        return datetime.combine(self.pickup_date, self.pickup_time)

    @property
    def return_datetime(self):
        return datetime.combine(self.return_date, self.return_time)

    def calculate_total_days(self):
        """
        Calculate total billable days between pickup and return.
        Any part of a day beyond a full 24-hour block counts as an extra day.
        Minimum is always 1 day.
        """
        delta = self.return_datetime - self.pickup_datetime
        if delta.total_seconds() <= 0:
            return 1
        days = delta.days
        remainder_seconds = delta.seconds
        if remainder_seconds > 0:
            days += 1
        return max(days, 1)

    def calculate_total_price(self):
        days = self.calculate_total_days()
        price = Decimal(days) * self.car.price_per_day
        return price

    def overlaps_with(self, other_pickup_dt, other_return_dt):
        """Check if this booking's date range overlaps with the given range."""
        return self.pickup_datetime < other_return_dt and other_pickup_dt < self.return_datetime

    def clean(self):
        errors = {}

        if self.pickup_date and self.return_date:
            if self.return_datetime <= self.pickup_datetime:
                errors['return_date'] = "Return date/time must be after the pickup date/time."

        if errors:
            raise ValidationError(errors)

    def check_double_booking(self):
        """
        Returns True if this booking's date range overlaps with any existing
        active (pending or approved) booking for the same car.
        """
        active_statuses = [self.STATUS_PENDING, self.STATUS_APPROVED]
        existing_qs = Booking.objects.filter(
            car=self.car,
            status__in=active_statuses,
        )
        if self.pk:
            existing_qs = existing_qs.exclude(pk=self.pk)

        new_pickup_dt = self.pickup_datetime
        new_return_dt = self.return_datetime

        for existing in existing_qs:
            if existing.overlaps_with(new_pickup_dt, new_return_dt):
                return True
        return False

    def save(self, *args, **kwargs):
        # Always recalculate days and price before saving to keep data consistent.
        self.total_days = self.calculate_total_days()
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    @property
    def can_be_cancelled(self):
        return self.status == self.STATUS_PENDING

    @property
    def status_badge_class(self):
        return {
            self.STATUS_PENDING: 'badge-pending',
            self.STATUS_APPROVED: 'badge-approved',
            self.STATUS_REJECTED: 'badge-rejected',
            self.STATUS_CANCELLED: 'badge-cancelled',
            self.STATUS_COMPLETED: 'badge-completed',
        }.get(self.status, 'badge-pending')
