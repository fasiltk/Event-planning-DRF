from django.db import models
from authentication.models import Authentication
from django.core.exceptions import ValidationError


class Event(models.Model):
    organizer = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'organizer'}  
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_seats = models.IntegerField()
    filled_seats = models.IntegerField(default=0)  

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        
        if self.organizer.role != 'organizer':
            raise ValidationError("Selected user is not an organizer")

        
        if self.filled_seats > self.total_seats:
            raise ValidationError("Filled seats cannot exceed total seats")

    def __str__(self):
        return self.title