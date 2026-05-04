from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer
from event.models import Event
from authentication.models import Authentication


def get_logged_in_user(request):
    email = request.session.get('email')

    if not email:
        return None

    try:
        return Authentication.objects.get(email=email)
    except Authentication.DoesNotExist:
        return None


# ──────────────────────────────────────────
# CREATE BOOKING
# ──────────────────────────────────────────

class CreateBookingView(APIView):

    def post(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'customer':
            return Response({"error": "Only customers can book"}, status=403)

        event_id = request.data.get('event')
        seats    = request.data.get('number_of_seats')

        if not event_id or not seats:
            return Response({"error": "Event and seats required"}, status=400)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        try:
            seats = int(seats)
        except:
            return Response({"error": "Seats must be number"}, status=400)

        if seats <= 0:
            return Response({"error": "Seats must be greater than 0"}, status=400)

        available = event.total_seats - event.filled_seats

        if seats > available:
            return Response({"error": f"Only {available} seats available"}, status=400)

        booking = Booking.objects.create(
            event          = event,
            customer       = user,
            number_of_seats= seats
        )

        event.filled_seats += seats
        event.save()

        return Response({
            "message"   : "Booking successful",
            "booking_id": booking.id
        }, status=201)


# ──────────────────────────────────────────
# MY BOOKINGS (Customer)
# ──────────────────────────────────────────

class MyBookingsView(APIView):

    def get(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'customer':
            return Response({"error": "Only customers allowed"}, status=403)

        bookings   = Booking.objects.filter(customer=user)
        serializer = BookingSerializer(bookings, many=True)

        return Response(serializer.data)


# ──────────────────────────────────────────
# CANCEL BOOKING
# ──────────────────────────────────────────

class CancelBookingView(APIView):

    def post(self, request, pk):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        try:
            booking = Booking.objects.get(id=pk, customer=user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        if booking.status == 'cancelled':
            return Response({"error": "Already cancelled"}, status=400)

        event               = booking.event
        event.filled_seats -= booking.seats_booked
        event.save()

        booking.status = 'cancelled'
        booking.save()

        return Response({"message": "Booking cancelled"})


# ──────────────────────────────────────────
# EVENT BOOKINGS (Organizer)
# ──────────────────────────────────────────

class EventBookingsView(APIView):

    def get(self, request, event_id):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'organizer':
            return Response({"error": "Only organizers allowed"}, status=403)

        try:
            event = Event.objects.get(id=event_id, organizer=user)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or not yours"}, status=404)

        bookings   = Booking.objects.filter(event=event)
        serializer = BookingSerializer(bookings, many=True)

        return Response(serializer.data)