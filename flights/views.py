from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView,FormView
from django.views.generic.base import RedirectView
from django.views import View
from .models import Flight, Client, CartItem, Ticket
from .forms import TicketForm, UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages


class HomeView(ListView):
    model = Flight
    template_name = 'flights/home.html'
    context_object_name = 'flights'

    def get_queryset(self):
        queryset = super().get_queryset()
        destination = self.request.GET.get('destination')
        flight_num = self.request.GET.get('flight_num')
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if flight_num:
            queryset = queryset.filter(flight_num__icontains=flight_num)
        return queryset

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'flights/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'flights/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')


class AddToCartView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('cart')
    def get_redirect_url(self, *args, **kwargs):
        flight_id = kwargs['flight_id']
        flight = get_object_or_404(Flight, id=flight_id)
        client = self.request.user.client
        cart_item, created = CartItem.objects.get_or_create(client=client, flight=flight, defaults={'quantity': 1})
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return super().get_redirect_url(*args, **kwargs)

class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'flights/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(client=self.request.user.client)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        for item in cart_items:
            item.total_price = item.flight.price * item.quantity
        return context

class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_item_id = kwargs['cart_item_id']
        cart_item = get_object_or_404(CartItem, id=cart_item_id, client=request.user.client)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully.')
        return redirect(reverse_lazy('cart'))


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client = request.user.client
        cart_items = CartItem.objects.filter(client=client)
        if not cart_items.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect(reverse_lazy('cart'))
        for cart_item in cart_items:
            flight = cart_item.flight
            if flight.total_num >= cart_item.quantity:
                flight.total_num -= cart_item.quantity
                flight.save()
                Ticket.objects.create(
                    flight=flight,
                    client=client,
                    quantity=cart_item.quantity
                    )
            else:
                messages.error(request, f"Sold out !  {flight.flight_num}.")
                return redirect(reverse_lazy('cart'))
        cart_items.delete()
        messages.success(request, 'Checkout successful.')
        return redirect(reverse_lazy('home'))


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client = request.user.client
        tickets = Ticket.objects.filter(client=client)
        context = {
               'tickets': tickets
                  }
        return render(request, 'flights/order.html', context)
