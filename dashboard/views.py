from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from bookings.models import Booking
from bookings.forms import BookingForm
from cars.models import Car
from cars.forms import CarForm
from .forms import DashboardLoginForm, BookingDecisionForm


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard_home')

    if request.method == 'POST':
        form = DashboardLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_username()}!")
            return redirect('dashboard:dashboard_home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = DashboardLoginForm()

    return render(request, 'dashboard/login.html', {'form': form})


@login_required
def dashboard_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('dashboard:login')


# ---------------------------------------------------------------------------
# Dashboard Home / Statistics
# ---------------------------------------------------------------------------

@login_required
def dashboard_home(request):
    today = timezone.localdate()

    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(is_available=True).count()

    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status=Booking.STATUS_PENDING).count()
    approved_bookings = Booking.objects.filter(status=Booking.STATUS_APPROVED).count()
    rejected_bookings = Booking.objects.filter(status=Booking.STATUS_REJECTED).count()
    cancelled_bookings = Booking.objects.filter(status=Booking.STATUS_CANCELLED).count()
    today_bookings = Booking.objects.filter(created_at__date=today).count()

    recent_bookings = Booking.objects.select_related('car').order_by('-created_at')[:8]

    context = {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'cancelled_bookings': cancelled_bookings,
        'today_bookings': today_bookings,
        'recent_bookings': recent_bookings,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/dashboard_home.html', context)


# ---------------------------------------------------------------------------
# Car Management
# ---------------------------------------------------------------------------

@login_required
def car_management(request):
    cars = Car.objects.all().order_by('-created_at')

    query = request.GET.get('q', '').strip()
    availability = request.GET.get('availability', '').strip()

    if query:
        cars = cars.filter(
            Q(brand__icontains=query) | Q(car_name__icontains=query) | Q(model__icontains=query)
        )

    if availability == 'available':
        cars = cars.filter(is_available=True)
    elif availability == 'unavailable':
        cars = cars.filter(is_available=False)

    paginator = Paginator(cars, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'cars': page_obj.object_list,
        'query': query,
        'selected_availability': availability,
        'page_title': 'Car Management',
    }
    return render(request, 'dashboard/car_management.html', context)


@login_required
def car_add(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, f"Car '{car.full_name}' added successfully.")
            return redirect('dashboard:car_management')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CarForm()

    context = {'form': form, 'page_title': 'Add New Car'}
    return render(request, 'dashboard/car_form.html', context)


@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()
            messages.success(request, f"Car '{car.full_name}' updated successfully.")
            return redirect('dashboard:car_management')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CarForm(instance=car)

    context = {'form': form, 'car': car, 'page_title': f'Edit {car.full_name}'}
    return render(request, 'dashboard/car_form.html', context)


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        car_name = car.full_name
        car.delete()
        messages.success(request, f"Car '{car_name}' deleted successfully.")
        return redirect('dashboard:car_management')

    context = {'car': car, 'page_title': f'Delete {car.full_name}'}
    return render(request, 'dashboard/car_delete_confirm.html', context)


# ---------------------------------------------------------------------------
# Booking Management
# ---------------------------------------------------------------------------

@login_required
def booking_management(request):
    bookings = Booking.objects.select_related('car').order_by('-created_at')

    status = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()

    if status:
        bookings = bookings.filter(status=status)

    if query:
        bookings = bookings.filter(
            Q(customer_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(car__brand__icontains=query) |
            Q(car__car_name__icontains=query)
        )

    paginator = Paginator(bookings, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'bookings': page_obj.object_list,
        'selected_status': status,
        'query': query,
        'status_choices': Booking.STATUS_CHOICES,
        'page_title': 'Booking Management',
    }
    return render(request, 'dashboard/booking_management.html', context)


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('car'), pk=pk)
    form = BookingDecisionForm(initial={'admin_note': booking.admin_note or ''})

    context = {
        'booking': booking,
        'form': form,
        'page_title': f'Booking #{booking.pk}',
    }
    return render(request, 'dashboard/booking_detail.html', context)


@login_required
def booking_approve(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        if booking.check_double_booking():
            messages.error(
                request,
                "Cannot approve this booking — it overlaps with another active booking for the same car."
            )
        else:
            form = BookingDecisionForm(request.POST)
            booking.status = Booking.STATUS_APPROVED
            if form.is_valid():
                booking.admin_note = form.cleaned_data.get('admin_note', '')
            booking.save()
            messages.success(request, f"Booking #{booking.pk} approved successfully.")

    return redirect('dashboard:booking_detail', pk=booking.pk)


@login_required
def booking_reject(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        form = BookingDecisionForm(request.POST)
        booking.status = Booking.STATUS_REJECTED
        if form.is_valid():
            booking.admin_note = form.cleaned_data.get('admin_note', '')
        booking.save()
        messages.success(request, f"Booking #{booking.pk} rejected.")

    return redirect('dashboard:booking_detail', pk=booking.pk)


@login_required
def booking_complete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        booking.status = Booking.STATUS_COMPLETED
        booking.save()
        messages.success(request, f"Booking #{booking.pk} marked as completed.")

    return redirect('dashboard:booking_detail', pk=booking.pk)


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f"Booking #{pk} deleted successfully.")
        return redirect('dashboard:booking_management')

    context = {'booking': booking, 'page_title': f'Delete Booking #{booking.pk}'}
    return render(request, 'dashboard/booking_delete_confirm.html', context)


# ---------------------------------------------------------------------------
# Customer List
# ---------------------------------------------------------------------------

@login_required
def customer_list(request):
    query = request.GET.get('q', '').strip()

    customers = (
        Booking.objects.values('customer_name', 'phone_number', 'email')
        .annotate(
            total_bookings=Count('id'),
            approved_count=Count('id', filter=Q(status=Booking.STATUS_APPROVED)),
            pending_count=Count('id', filter=Q(status=Booking.STATUS_PENDING)),
        )
        .order_by('customer_name')
    )

    if query:
        customers = customers.filter(
            Q(customer_name__icontains=query) | Q(phone_number__icontains=query)
        )

    paginator = Paginator(list(customers), 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'customers': page_obj.object_list,
        'query': query,
        'page_title': 'Customer List',
    }
    return render(request, 'dashboard/customer_list.html', context)


@login_required
def customer_detail(request, phone_number):
    bookings = Booking.objects.select_related('car').filter(
        phone_number=phone_number
    ).order_by('-created_at')

    if not bookings.exists():
        messages.error(request, "No customer found with this phone number.")
        return redirect('dashboard:customer_list')

    customer_name = bookings.first().customer_name
    email = bookings.first().email

    context = {
        'bookings': bookings,
        'customer_name': customer_name,
        'phone_number': phone_number,
        'email': email,
        'page_title': f'Customer: {customer_name}',
    }
    return render(request, 'dashboard/customer_detail.html', context)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

@login_required
def reports(request):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)

    total_revenue = Booking.objects.filter(
        status__in=[Booking.STATUS_APPROVED, Booking.STATUS_COMPLETED]
    ).aggregate(total=Sum('total_price'))['total'] or 0

    month_revenue = Booking.objects.filter(
        status__in=[Booking.STATUS_APPROVED, Booking.STATUS_COMPLETED],
        created_at__date__gte=start_of_month,
    ).aggregate(total=Sum('total_price'))['total'] or 0

    bookings_by_status = (
        Booking.objects.values('status').annotate(count=Count('id')).order_by('status')
    )

    top_cars = (
        Booking.objects.values('car__brand', 'car__car_name', 'car__model')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')[:5]
    )

    monthly_bookings = Booking.objects.filter(created_at__date__gte=start_of_month).count()

    context = {
        'total_revenue': total_revenue,
        'month_revenue': month_revenue,
        'bookings_by_status': bookings_by_status,
        'top_cars': top_cars,
        'monthly_bookings': monthly_bookings,
        'total_cars': Car.objects.count(),
        'total_bookings': Booking.objects.count(),
        'page_title': 'Reports',
    }
    return render(request, 'dashboard/reports.html', context)
