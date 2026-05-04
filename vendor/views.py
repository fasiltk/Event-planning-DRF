from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import VendorRequest
from .serializers import VendorRequestSerializer
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
# SEND REQUEST (Vendor only)
# ──────────────────────────────────────────

class SendRequestView(APIView):

    def post(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'vendor':
            return Response({"error": "Only vendors allowed"}, status=403)

        event_id = request.data.get('event')

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        serializer = VendorRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(vendor=user, event=event)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ──────────────────────────────────────────
# MY REQUESTS (Vendor)
# ──────────────────────────────────────────

class MyRequestsView(APIView):

    def get(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'vendor':
            return Response({"error": "Only vendors allowed"}, status=403)

        requests   = VendorRequest.objects.filter(vendor=user)
        serializer = VendorRequestSerializer(requests, many=True)

        return Response(serializer.data)


# ──────────────────────────────────────────
# EVENT REQUESTS (Organizer)
# ──────────────────────────────────────────

class EventRequestsView(APIView):

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

        requests   = VendorRequest.objects.filter(event=event)
        serializer = VendorRequestSerializer(requests, many=True)

        return Response(serializer.data)


# ──────────────────────────────────────────
# UPDATE REQUEST STATUS (Organizer)
# ──────────────────────────────────────────

class UpdateRequestStatusView(APIView):

    def post(self, request, pk):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Login required"}, status=401)

        if user.role != 'organizer':
            return Response({"error": "Only organizers allowed"}, status=403)

        try:
            vendor_request = VendorRequest.objects.get(id=pk)
        except VendorRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

        if vendor_request.event.organizer != user:
            return Response({"error": "Not your event"}, status=403)

        new_status = request.data.get('status')

        if new_status not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status"}, status=400)

        vendor_request.status = new_status
        vendor_request.save()

        return Response({"message": f"Request {new_status}"})