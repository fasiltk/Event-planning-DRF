from django.db import models

from event.models import Event
from authentication.models import Authentication
# Create your models here.
class VendorRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    vendor = models.ForeignKey(
        Authentication,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'vendor'}
    )

    service_type = models.CharField(max_length=100)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)