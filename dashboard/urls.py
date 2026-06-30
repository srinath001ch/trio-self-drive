from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),

    # Dashboard home
    path('', views.dashboard_home, name='dashboard_home'),

    # Car management
    path('cars/', views.car_management, name='car_management'),
    path('cars/add/', views.car_add, name='car_add'),
    path('cars/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('cars/<int:pk>/delete/', views.car_delete, name='car_delete'),

    # Booking management
    path('bookings/', views.booking_management, name='booking_management'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/approve/', views.booking_approve, name='booking_approve'),
    path('bookings/<int:pk>/reject/', views.booking_reject, name='booking_reject'),
    path('bookings/<int:pk>/complete/', views.booking_complete, name='booking_complete'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<str:phone_number>/', views.customer_detail, name='customer_detail'),

    # Reports
    path('reports/', views.reports, name='reports'),
]
