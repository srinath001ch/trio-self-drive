from django.contrib import admin
from django.utils.html import format_html
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'full_name', 'brand', 'price_per_day', 'fuel_type',
                     'transmission', 'seats', 'is_available', 'created_at')
    list_filter = ('brand', 'fuel_type', 'transmission', 'is_available')
    search_fields = ('brand', 'car_name', 'model')
    list_editable = ('is_available',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Car Information', {
            'fields': ('brand', 'car_name', 'model', 'image')
        }),
        ('Specifications', {
            'fields': ('price_per_day', 'fuel_type', 'transmission', 'seats', 'mileage')
        }),
        ('Description & Availability', {
            'fields': ('description', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Image"
