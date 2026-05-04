from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateEventView.as_view()),
    path('my-events/', MyEventsView.as_view()),
    path('all/', AllEventsView.as_view()),
    path('detail/<int:pk>/', EventDetailView.as_view()),
    path('update/<int:pk>/', UpdateEventView.as_view()),
    path('delete/<int:pk>/', DeleteEventView.as_view()),
]