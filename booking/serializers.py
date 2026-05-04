from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['customer']

    def validate_number_of_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of seats must be greater than 0")
        return value