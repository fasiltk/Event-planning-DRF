from django.urls import path
from .views import *

urlpatterns = [
    path('book/', CreateBookingView.as_view()),
    path('my-bookings/', MyBookingsView.as_view()),
    path('cancel/<int:pk>/', CancelBookingView.as_view()),
    path('event-bookings/<int:event_id>/', EventBookingsView.as_view()),
]