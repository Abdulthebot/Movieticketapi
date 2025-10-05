from django.db import models
from django.conf import settings
from apps.movies.models import Show

class Booking(models.Model):
    # Using TextChoices for status prevents errors from raw string comparisons[cite: 60].
    class Status(models.TextChoices):
        BOOKED = 'BOOKED', 'Booked'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.BOOKED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # A unique constraint prevents a user from double-booking the same seat for the same show[cite: 97].
        unique_together = ('show', 'seat_number', 'status')
        constraints = [
            models.UniqueConstraint(
                fields=['show', 'seat_number'],
                condition=models.Q(status='BOOKED'),
                name='unique_booked_seat_for_show'
            )
        ]

    def __str__(self):
        return f"Booking for {self.user.email} - Seat {self.seat_number} for Show {self.show.id}"