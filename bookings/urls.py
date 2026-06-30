from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:pk>/', views.book_car, name='book_car'),
    path('success/<int:pk>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.booking_search, name='booking_search'),
    path('status/<int:pk>/', views.booking_status, name='booking_status'),
    path('cancel/<int:pk>/', views.booking_cancel, name='booking_cancel'),
]
