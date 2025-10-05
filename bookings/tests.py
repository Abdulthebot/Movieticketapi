from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.movies.models import Movie, Show
from .models import Booking

User = get_user_model()

# The test suite uses APITestCase to verify core business logic[cite: 288].
class BookingAPITests(APITestCase):

    def setUp(self):
        """Set up the test environment."""
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='password123')
        
        self.movie = Movie.objects.create(title='Inception', duration_minutes=148)
        self.show = Show.objects.create(movie=self.movie, screen_name='Screen 1', date_time='2025-12-25T20:00:00Z', total_seats=50)
        
        # Authenticate the client for requests[cite: 291].
        self.client.force_authenticate(user=self.user)

    def test_successful_booking(self):
        """
        Ensures an authenticated user can successfully book an available seat[cite: 294].
        """
        url = reverse('book-seat', kwargs={'show_id': self.show.id})
        data = {'seat_number': 10}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().seat_number, 10)
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_booking_a_taken_seat(self):
        """
        Ensures attempting to book an already taken seat fails with a 400 error[cite: 295].
        """
        # First booking is successful
        Booking.objects.create(user=self.user, show=self.show, seat_number=25, status=Booking.Status.BOOKED)
        
        # Second attempt to book the same seat
        url = reverse('book-seat', kwargs={'show_id': self.show.id})
        data = {'seat_number': 25}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already booked', str(response.data))

    def test_unauthorized_booking_attempt(self):
        """
        Ensures an unauthenticated user cannot book a seat[cite: 296].
        """
        self.client.force_authenticate(user=None) # Log out the user
        url = reverse('book-seat', kwargs={'show_id': self.show.id})
        data = {'seat_number': 5}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_successful_cancellation(self):
        """
        Ensures a user can cancel their own booking[cite: 297].
        """
        booking = Booking.objects.create(user=self.user, show=self.show, seat_number=30, status=Booking.Status.BOOKED)
        url = reverse('cancel-booking', kwargs={'booking_id': booking.id})
        
        response = self.client.post(url)
        booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(booking.status, Booking.Status.CANCELLED)

    def test_permission_denied_on_cancellation(self):
        """
        Verifies a user gets a 403 Forbidden error when trying to cancel another user's booking[cite: 298].
        """
        # A booking made by another user
        other_users_booking = Booking.objects.create(user=self.other_user, show=self.show, seat_number=40)
        
        url = reverse('cancel-booking', kwargs={'booking_id': other_users_booking.id})
        
        # The authenticated user (self.user) tries to cancel the other user's booking
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)