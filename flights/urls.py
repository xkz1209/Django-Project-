from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('add_to_cart/<int:flight_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('remove_from_cart/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('search_flights/', views.HomeView.as_view(), name='search_flights'),
    path('orders/', views.OrderView.as_view(), name='orders'),
]
