from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    
    path('', AccountViews.customerDashboard, name='customer'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('my_orders/', views.my_orders, name='customer_orders'),
    path('order_details/<int:order_number>/', views.order_details, name='order_details')
]
