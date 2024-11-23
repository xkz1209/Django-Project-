from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_num = models.CharField(max_length=10)
    destination = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_time = models.DateTimeField()
    num_stops = models.IntegerField(default=0)
    flight_type = models.CharField(max_length=50)

    total_num = models.IntegerField(default=100)

    def __str__(self):
        return f"Flight {self.flight_num} to {self.destination}"

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    passport_id = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='client_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_placed_date = models.DateTimeField(auto_now_add=True)
    #total_num = models.IntegerField()
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  

    def save(self, *args, **kwargs):
        self.total_price = self.flight.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Ticket for {self.client} on {self.flight}"

class CartItem(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  

    def save(self, *args, **kwargs):
        self.total_price = self.flight.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CartItem for {self.client} on {self.flight}"
