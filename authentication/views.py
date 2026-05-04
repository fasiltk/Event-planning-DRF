from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Authentication
from .serializers import RegisterSerializer, LoginSerializer


def get_logged_in_user(request):
    email = request.session.get('email')

    if not email:
        return None

    try:
        user = Authentication.objects.get(email=email)
        return user
    except Authentication.DoesNotExist:
        return None


# ──────────────────────────────────────────
# REGISTER
# ──────────────────────────────────────────

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registered successfully"}, status=201)

        return Response(serializer.errors, status=400)


# ──────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email    = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = Authentication.objects.get(email=email)
            except Authentication.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=400)

            if user.password == password:
                request.session['email'] = user.email

                return Response({
                    "message": "Login successful",
                    "email"  : user.email,
                    "role"   : user.role
                })

            return Response({"error": "Invalid credentials"}, status=400)

        return Response(serializer.errors, status=400)


# ──────────────────────────────────────────
# LOGOUT
# ──────────────────────────────────────────

class LogoutView(APIView):

    def post(self, request):
        request.session.flush()
        return Response({"message": "Logged out successfully"})

    def get(self, request):
        request.session.flush()
        return Response({"message": "Logged out successfully"})


# ──────────────────────────────────────────
# PROFILE
# ──────────────────────────────────────────

class ProfileView(APIView):

    def get(self, request):
        user = get_logged_in_user(request)

        if not user:
            return Response({"error": "Not logged in"}, status=401)

        return Response({
            "name" : user.name,
            "email": user.email,
            "role" : user.role
        })