from django.contrib.auth.models import AbstractUser
from django.db import models

# Inheriting from AbstractUser provides flexibility for future enhancements[cite: 36, 44].
class User(AbstractUser):
    # Using email as the unique identifier is a modern practice for user authentication[cite: 46, 47].
    email = models.EmailField(unique=True, blank=False, error_messages={'unique': "A user with that email already exists."})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email