from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Booking, Show
from .serializers import BookingCreationSerializer, BookingListSerializer
from apps.core.permissions import IsBookingOwner

class BookSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # The entire booking process is wrapped in an atomic transaction to ensure data integrity[cite: 167].
    @transaction.atomic
    def post(self, request, show_id):
        try:
            # Pessimistic locking acquires a row-level lock on the Show object to prevent race conditions[cite: 172].
            show = Show.objects.select_for_update().get(pk=show_id)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingCreationSerializer(
            data=request.data,
            context={'request': request, 'show': show}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingListView(generics.ListAPIView):
    """
    API view to retrieve all bookings made by the logged-in user.
    """
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    # The queryset is filtered to only return bookings belonging to the authenticated user[cite: 153].
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class CancelBookingView(APIView):
    """
    API view to cancel a specific booking owned by the user.
    """
    permission_classes = [permissions.IsAuthenticated, IsBookingOwner]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        self.check_object_permissions(request, booking) # This line explicitly triggers the IsBookingOwner permission check.

        if booking.status == Booking.Status.CANCELLED:
            return Response({"message": "This booking has already been cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = Booking.Status.CANCELLED
        booking.save()
        return Response({"status": "Booking successfully cancelled."}, status=status.HTTP_200_OK)