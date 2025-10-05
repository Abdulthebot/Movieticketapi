from django.urls import path
from .views import BookSeatView, BookingListView, CancelBookingView

urlpatterns = [
    path('shows/<int:show_id>/book/', BookSeatView.as_view(), name='book-seat'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
]