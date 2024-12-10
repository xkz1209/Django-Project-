#Kaizhe Xu(kax225@bu.edu) Description: This is the admin file for flight,client,ticket,and baggage
from django.contrib import admin
from .models import Flight, Client, Ticket,CartItem,Baggage

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_num', 'destination', 'departure', 'price', 'departure_time', 'num_stops', 'flight_type','total_num')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'passport_id', 'date_of_birth', 'gender', 'phone_number')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('flight', 'client', 'order_placed_date', 'quantity','total_price')

@admin.register(CartItem)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('flight', 'client', 'quantity','total_price')

@admin.register(Baggage)
class BaggageAdmin(admin.ModelAdmin):
        list_display = ('ticket', 'onboard', 'passenger_count','is_member','has_delta_card','is_checkout')
