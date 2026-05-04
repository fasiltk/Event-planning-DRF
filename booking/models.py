from django.db import models
from event.models import Event
from authentication.models import Authentication
from django.core.exceptions import ValidationError
# Create your models here.
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    customer = models.ForeignKey(Authentication, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_seats = models.IntegerField()

    def __str__(self):
        return f"Booking for {self.event.title} by {self.customer.email}"
    
    def clean(self):
        # ✅ ensure customer role
        if self.customer.role != 'customer':
            raise ValidationError("Selected user is not a customer")

        # ✅ check seat availability
        if self.number_of_seats <= 0:
            raise ValidationError("Number of seats must be positive")

        if self.event.filled_seats + self.number_of_seats > self.event.total_seats:
            raise ValidationError("Not enough seats available for this event")