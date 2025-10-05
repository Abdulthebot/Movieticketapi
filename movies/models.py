from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    duration_minutes = models.PositiveIntegerField(help_text="Duration of the movie in minutes.")

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.title} at {self.screen_name} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"