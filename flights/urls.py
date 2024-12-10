#Kaizhe Xu(kax225@bu.edu) Description: This is the url file for shopping cart, authentication, order history and passengager services.
from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),

    # User authentication and account management
    path('register/', views.RegisterView.as_view(), name='register'),  # Registration page
    path('login/', views.LoginView.as_view(), name='login'),           # Login page
    path('logout/', views.LogoutView.as_view(), name='logout'),         # Logout functionality

    # Shopping cart related URLs
    path('add_to_cart/<int:flight_id>/', views.AddToCartView.as_view(), name='add_to_cart'),  # Add a flight to the cart
    path('cart/', views.CartView.as_view(), name='cart'),               # View the shopping cart
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),   # Checkout process
    path('remove_from_cart/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),  # Remove an item from the cart

    # Search for flights (reusing HomeView for simplicity)
    path('search_flights/', views.HomeView.as_view(), name='search_flights'),

    # Order history
    path('orders/', views.OrderView.as_view(), name='orders'),          # View past orders

    # Passenger services
    path('check_in/<int:ticket_id>/', views.CheckInView.as_view(), name='check_in'),  # Check-in process for a specific ticket
    path('baggage/<int:ticket_id>/', views.BaggageView.as_view(), name='baggage'),    # Baggage handling for a specific ticket
]