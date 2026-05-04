from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Event
from .serializers import EventSerializer
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
# CREATE EVENT (Organizer only)
# ──────────────────────────────────────────

class CreateEventView(APIView):

    def post(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'organizer':
            return Response({"error": "Only organizers allowed"}, status=403)

        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(organizer=user, filled_seats=0)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ──────────────────────────────────────────
# MY EVENTS
# ──────────────────────────────────────────

class MyEventsView(APIView):

    def get(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        events     = Event.objects.filter(organizer=user)
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)


# ──────────────────────────────────────────
# ALL EVENTS
# ──────────────────────────────────────────

class AllEventsView(APIView):

    def get(self, request):
        events     = Event.objects.all()
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)


# ──────────────────────────────────────────
# EVENT DETAIL
# ──────────────────────────────────────────

class EventDetailView(APIView):

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        data                    = EventSerializer(event).data
        data['available_seats'] = event.total_seats - event.filled_seats

        return Response(data)


# ──────────────────────────────────────────
# UPDATE EVENT
# ──────────────────────────────────────────

class UpdateEventView(APIView):

    def put(self, request, pk):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        try:
            event = Event.objects.get(id=pk, organizer=user)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or not yours"}, status=404)

        serializer = EventSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            updated_event = serializer.save()

            if updated_event.filled_seats > updated_event.total_seats:
                return Response({"error": "Filled seats cannot exceed total seats"}, status=400)

            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# ──────────────────────────────────────────
# DELETE EVENT
# ──────────────────────────────────────────

class DeleteEventView(APIView):

    def delete(self, request, pk):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        try:
            event = Event.objects.get(id=pk, organizer=user)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or not yours"}, status=404)

        event.delete()
        return Response({"message": "Deleted successfully"})