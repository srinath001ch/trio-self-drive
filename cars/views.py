from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Car


def car_list(request):
    """Public car listing page with simple search and filters."""
    cars = Car.objects.filter(is_available=True)

    query = request.GET.get('q', '').strip()
    fuel_type = request.GET.get('fuel_type', '').strip()
    transmission = request.GET.get('transmission', '').strip()
    sort = request.GET.get('sort', '').strip()

    if query:
        cars = cars.filter(
            Q(brand__icontains=query) |
            Q(car_name__icontains=query) |
            Q(model__icontains=query)
        )

    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)

    if transmission:
        cars = cars.filter(transmission=transmission)

    if sort == 'price_low':
        cars = cars.order_by('price_per_day')
    elif sort == 'price_high':
        cars = cars.order_by('-price_per_day')
    else:
        cars = cars.order_by('-created_at')

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cars': page_obj.object_list,
        'query': query,
        'selected_fuel_type': fuel_type,
        'selected_transmission': transmission,
        'selected_sort': sort,
        'fuel_type_choices': Car.FUEL_TYPE_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'page_title': 'Our Cars',
    }
    return render(request, 'cars/car_list.html', context)


def car_detail(request, pk):
    """Public car detail page showing specs and a booking call-to-action."""
    car = get_object_or_404(Car, pk=pk)
    related_cars = Car.objects.filter(
        is_available=True, brand=car.brand
    ).exclude(pk=car.pk)[:3]

    context = {
        'car': car,
        'related_cars': related_cars,
        'page_title': car.full_name,
    }
    return render(request, 'cars/car_detail.html', context)
