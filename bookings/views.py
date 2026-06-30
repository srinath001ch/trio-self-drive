from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from cars.models import Car
from .forms import BookingForm, BookingSearchForm
from .models import Booking


def book_car(request, pk):
    """Public booking page for a specific car. No login required."""
    car = get_object_or_404(Car, pk=pk)

    if not car.is_available:
        messages.warning(request, "Sorry, this car is currently unavailable for booking.")
        return redirect('cars:car_detail', pk=car.pk)

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES, car=car)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.status = Booking.STATUS_PENDING
            booking.save()
            messages.success(
                request,
                "Your booking request has been submitted successfully! "
                "We will contact you shortly to confirm your booking."
            )
            return redirect('bookings:booking_success', pk=booking.pk)
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = BookingForm(car=car)

    context = {
        'form': form,
        'car': car,
        'page_title': f'Book {car.full_name}',
    }
    return render(request, 'bookings/book_car.html', context)


def booking_success(request, pk):
    """Confirmation page shown right after a booking is submitted."""
    booking = get_object_or_404(Booking, pk=pk)
    context = {'booking': booking, 'page_title': 'Booking Submitted'}
    return render(request, 'bookings/booking_success.html', context)


def booking_search(request):
    """Customers search their bookings by phone number (no account needed)."""
    form = BookingSearchForm(request.GET or None)
    bookings = None
    searched = False

    if request.GET and form.is_valid():
        phone_number = form.cleaned_data['phone_number']
        digits = ''.join(filter(str.isdigit, phone_number))
        bookings = Booking.objects.filter(phone_number__icontains=digits[-10:])
        searched = True

    context = {
        'form': form,
        'bookings': bookings,
        'searched': searched,
        'page_title': 'My Bookings',
    }
    return render(request, 'bookings/booking_search.html', context)


def booking_status(request, pk):
    """Detail page showing the status of a single booking."""
    booking = get_object_or_404(Booking, pk=pk)
    context = {'booking': booking, 'page_title': 'Booking Status'}
    return render(request, 'bookings/booking_status.html', context)


def booking_cancel(request, pk):
    """Allow a customer to cancel their own booking if it is still pending."""
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        if booking.can_be_cancelled:
            booking.status = Booking.STATUS_CANCELLED
            booking.save()
            messages.success(request, "Your booking has been cancelled successfully.")
        else:
            messages.error(
                request,
                "This booking cannot be cancelled because it is no longer pending."
            )
        return redirect('bookings:booking_status', pk=booking.pk)

    context = {'booking': booking, 'page_title': 'Cancel Booking'}
    return render(request, 'bookings/booking_cancel_confirm.html', context)
