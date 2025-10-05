from rest_framework import serializers
from .models import Booking

class BookingCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['seat_number']

    # Field-level validation ensures the seat number is within the valid range for the show[cite: 221].
    def validate_seat_number(self, value):
        show = self.context['show']
        if not (1 <= value <= show.total_seats):
            raise serializers.ValidationError(f"Seat number must be between 1 and {show.total_seats}.")
        return value

    # Object-level validation enforces complex business rules like preventing overbooking and double-booking[cite: 224].
    def validate(self, data):
        show = self.context['show']
        seat_number = data.get('seat_number')

        # Check for double booking
        if Booking.objects.filter(show=show, seat_number=seat_number, status=Booking.Status.BOOKED).exists():
            raise serializers.ValidationError(f"Seat {seat_number} is already booked for this show.")

        # Check for overbooking (This check is theoretically redundant due to the pessimistic lock but serves as a good safeguard)
        booked_seats_count = Booking.objects.filter(show=show, status=Booking.Status.BOOKED).count()
        if booked_seats_count >= show.total_seats:
            raise serializers.ValidationError("This show is fully booked.")
            
        return data

    def create(self, validated_data):
        booking = Booking.objects.create(
            user=self.context['request'].user,
            show=self.context['show'],
            **validated_data
        )
        return booking

class BookingListSerializer(serializers.ModelSerializer):
    show = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'show', 'seat_number', 'status', 'created_at']