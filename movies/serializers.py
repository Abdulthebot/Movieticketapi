from rest_framework import serializers
from .models import Movie, Show
from apps.bookings.models import Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes']

class ShowSerializer(serializers.ModelSerializer):
    # available_seats is dynamically calculated to provide real-time seat availability[cite: 146].
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'movie', 'screen_name', 'date_time', 'total_seats', 'available_seats']
        read_only_fields = ['movie']

    def get_available_seats(self, obj):
        booked_seats_count = Booking.objects.filter(show=obj, status=Booking.Status.BOOKED).count()
        return obj.total_seats - booked_seats_count