from django.contrib import messages
from django.shortcuts import render, redirect

from cars.models import Car
from .forms import ContactForm
from .models import FAQ, Testimonial


def home(request):
    """Homepage with hero banner, featured cars, why-choose-us, how-it-works, FAQ preview."""
    featured_cars = Car.objects.filter(is_available=True).order_by('-created_at')[:6]
    faqs = FAQ.objects.filter(is_active=True)[:5]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    total_cars = Car.objects.count()

    context = {
        'featured_cars': featured_cars,
        'faqs': faqs,
        'testimonials': testimonials,
        'total_cars': total_cars,
        'page_title': 'Home',
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {'page_title': 'About Us'}
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you for reaching out! Our team will get back to you shortly."
            )
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = ContactForm()

    context = {'form': form, 'page_title': 'Contact Us'}
    return render(request, 'core/contact.html', context)


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    context = {'faqs': faqs, 'page_title': 'Frequently Asked Questions'}
    return render(request, 'core/faq.html', context)
