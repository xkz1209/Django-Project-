from django.db import models
from django.contrib.auth.models import User
import random
import string

class Flight(models.Model):
    # Flight information fields
    flight_num = models.CharField(max_length=10)  # Unique flight number
    destination = models.CharField(max_length=100)  # Destination city or airport
    departure = models.CharField(max_length=100)  # Departure city or airport
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per seat
    departure_time = models.DateTimeField()  # Scheduled departure time
    num_stops = models.IntegerField(default=0)  # Number of stops during the flight
    flight_type = models.CharField(max_length=50)  # Type of flight (e.g., domestic, international)

    total_num = models.IntegerField(default=100)  # Total number of seats available

    def __str__(self):
        return f"Flight {self.flight_num} to {self.destination}"  # String representation for admin interface

class Client(models.Model):
    # Client profile linked to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    passport_id = models.CharField(max_length=50)  # Passport ID for identification
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='client_photos/', blank=True, null=True)  # Optional client photo

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # String representation for admin interface

class Baggage(models.Model):
    # Baggage information linked to a Ticket
    ticket = models.OneToOneField('Ticket', related_name='baggage', on_delete=models.CASCADE)  # One-to-one relationship with Ticket

    CABIN_CHOICES = [
        ('first_cabin', 'First Cabin'),  # Actual stored value, human-readable label
        ('second_cabin', 'Second Cabin')
    ]
    onboard = models.CharField(max_length=20, choices=CABIN_CHOICES, default='second_cabin')  # Cabin type
    passenger_count = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=1)  # Number of passengers
    is_member = models.BooleanField(default=False)  # Whether the passenger is a member
    has_delta_card = models.BooleanField(default=False)  # Whether the passenger has a Delta card
    is_checkout = models.BooleanField(default=False)  # Whether the baggage has been checked out

class Ticket(models.Model):
    # Ticket information linking a Client to a Flight
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Many-to-one relationship with Flight
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Many-to-one relationship with Client
    order_placed_date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when the ticket is created
    quantity = models.IntegerField()  # Number of tickets purchased
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total price of tickets

    checked_in = models.BooleanField(default=False)  # Whether the ticket has been checked in
    seat_number = models.JSONField(null=True, blank=True)  # JSON field for storing seat numbers

    def save(self, *args, **kwargs):
        self.total_price = self.flight.price * self.quantity  # Calculate total price before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket for {self.client} on {self.flight}"  # String representation for admin interface

    def check_in(self):
        self.checked_in = True
        self.seat_number = [self.generate_seat_number() for _ in range(self.quantity)]  # Generate seat numbers
        self.save()

    def generate_seat_number(self):
        row = random.randint(1, 20)  # Random row number between 1 and 20
        column = random.choice(string.ascii_uppercase[:6])  # Random column letter A-F
        return f"{row}{column}"  # Combine row and column into a seat number

class CartItem(models.Model):
    # Shopping cart item linking a Client to a Flight
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Many-to-one relationship with Client
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Many-to-one relationship with Flight
    quantity = models.IntegerField(default=1)  # Number of tickets added to cart
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total price of items in cart

    def save(self, *args, **kwargs):
        self.total_price = self.flight.price * self.quantity  # Calculate total price before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CartItem for {self.client} on {self.flight}"  # String representation for admin interface