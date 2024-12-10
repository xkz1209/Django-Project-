#Kaizhe Xu(kax225@bu.edu) Description: This is the view file for baggage,checkin, Loginin, Loginout, cartView and CartRemove
#Cart part has some specific functions whose corresponding views are AddtoCartView, CartView, RemoveFromCartView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, FormView
from django.views.generic.base import RedirectView
from django.views import View
from .models import Flight, Client, CartItem, Ticket, Baggage
from .forms import TicketForm, UserRegisterForm, UserLoginForm, BaggageForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

class BaggageView(View):
    """
    Handles baggage information for a specific ticket.
    """
    template_name = 'flights/baggage.html'

    def get(self, request, ticket_id):
        """
        Displays the form to update baggage details.
        """
        ticket = get_object_or_404(Ticket, id=ticket_id)
        baggage, created = Baggage.objects.get_or_create(ticket=ticket, defaults={'is_checkout': False})
        form = BaggageForm(instance=baggage)
        context = {
            'ticket': ticket,
            'form': form,
            'is_checkout': baggage.is_checkout,
            'baggage': baggage
        }
        return render(request, self.template_name, context)

    def post(self, request, ticket_id):
        """
        Processes the form submission to save updated baggage details.
        """
        ticket = get_object_or_404(Ticket, id=ticket_id)
        baggage, created = Baggage.objects.get_or_create(ticket=ticket, defaults={'is_checkout': False})
        form = BaggageForm(request.POST, instance=baggage)
        if form.is_valid():
            baggage = form.save(commit=False)
            baggage.is_checkout = True
            baggage.save()
            return redirect(reverse_lazy('orders'))
        context = {
            'ticket': ticket,
            'form': form,
            'is_checkout': baggage.is_checkout,
            'baggage': baggage
        }
        return render(request, self.template_name, context)

class CheckInView(View):
    """
    Handles check-in process for a specific ticket.
    """
    def get(self, request, ticket_id):
        """
        Checks if it's appropriate time for check-in and processes check-in.
        """
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.flight.departure_time > timezone.now() + timedelta(days=3):
            messages.error(request, 'Too early to checkin.')
        elif ticket.flight.departure_time < timezone.now():
            messages.error(request, 'Have taken off.')
        elif not ticket.checked_in:
            ticket.check_in()
            messages.success(request, 'Checkin successful.')
        else:
            messages.warning(request, 'Already checked in.')
        return redirect(reverse_lazy('orders'))

class HomeView(ListView):
    """
    Lists all flights with optional filtering.
    """
    model = Flight
    template_name = 'flights/home.html'
    context_object_name = 'flights'

    def get_queryset(self):
        """
        Filters flights based on user input from GET parameters.
        """
        queryset = super().get_queryset()
        destination = self.request.GET.get('destination')
        flight_num = self.request.GET.get('flight_num')
        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if flight_num:
            queryset = queryset.filter(flight_num__icontains=flight_num)
        if min_price is not None and min_price.strip():
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None and max_price.strip():
            queryset = queryset.filter(price__lte=max_price)
        return queryset

class RegisterView(CreateView):
    """
    Allows users to register a new account.
    """
    form_class = UserRegisterForm
    template_name = 'flights/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class LoginView(FormView):
    """
    Allows users to log into their accounts.
    """
    form_class = UserLoginForm
    template_name = 'flights/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class LogoutView(LoginRequiredMixin, View):
    """
    Logs out the current user.
    """
    def get(self, request):
        logout(request)
        return redirect('home')

class AddToCartView(LoginRequiredMixin, RedirectView):
    """
    Adds a flight to the user's cart.
    """
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
    """
    Displays the user's shopping cart.
    """
    model = CartItem
    template_name = 'flights/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(client=self.request.user.client)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        for item in cart_items:
            item.total_price = item.flight.price * item.quantity
        return context

class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Removes an item from the user's cart.
    """
    def get(self, request, *args, **kwargs):
        cart_item_id = kwargs['cart_item_id']
        cart_item = get_object_or_404(CartItem, id=cart_item_id, client=request.user.client)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully.')
        return redirect(reverse_lazy('cart'))

class CheckoutView(LoginRequiredMixin, View):
    """
    Processes checkout of items in the cart and creates tickets.
    """
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
    """
    Displays the user's order history.
    """
    def get(self, request, *args, **kwargs):
        client = request.user.client
        tickets = Ticket.objects.filter(client=client).select_related('baggage')
        context = {'tickets': tickets}
        return render(request, 'flights/order.html', context)