from django.contrib import admin
from .models import ContactMessage, FAQ, Testimonial


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'phone_number', 'email', 'subject')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('rating', 'is_active')
