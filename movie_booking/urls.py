from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# This configuration sets up the main schema view for Swagger UI[cite: 365].
schema_view = get_schema_view(
   openapi.Info(
      title="Movie Ticket Booking API",
      default_version='v1',
      description="API documentation for the Movie Ticket Booking System",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints are versioned under /api/v1/ for future-proofing.
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/', include('apps.movies.urls')),
    path('api/v1/', include('apps.bookings.urls')),

    # Swagger UI endpoint [cite: 379]
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]