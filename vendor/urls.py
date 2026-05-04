from django.urls import path
from .views import (
    SendRequestView,
    MyRequestsView,
    EventRequestsView,
    UpdateRequestStatusView
)

urlpatterns = [
    path('send/', SendRequestView.as_view()),
    path('my-requests/', MyRequestsView.as_view()),
    path('event-requests/<int:event_id>/', EventRequestsView.as_view()),
    path('update-status/<int:pk>/', UpdateRequestStatusView.as_view()),
]