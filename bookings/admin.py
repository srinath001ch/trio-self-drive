from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'car', 'pickup_date',
                     'return_date', 'total_days', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'pickup_date', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'email', 'car__brand', 'car__car_name')
    readonly_fields = ('total_days', 'total_price', 'created_at', 'updated_at')
    list_editable = ('status',)

    fieldsets = (
        ('Car & Customer', {
            'fields': ('car', 'customer_name', 'phone_number', 'email', 'driving_license')
        }),
        ('Rental Period', {
            'fields': ('pickup_date', 'pickup_time', 'return_date', 'return_time')
        }),
        ('Pricing (Auto-calculated)', {
            'fields': ('total_days', 'total_price')
        }),
        ('Status', {
            'fields': ('status', 'admin_note')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
