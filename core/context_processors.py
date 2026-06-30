"""
Context processors for the core app.
Makes business/site information available in every template automatically.
"""
from django.conf import settings


def site_settings(request):
    """Inject site-wide business information into every template context."""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'BUSINESS_PHONE': settings.BUSINESS_PHONE,
        'BUSINESS_PHONE_DISPLAY': settings.BUSINESS_PHONE_DISPLAY,
        'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER,
        'BUSINESS_EMAIL': settings.BUSINESS_EMAIL,
        'BUSINESS_ADDRESS': settings.BUSINESS_ADDRESS,
    }
