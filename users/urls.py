from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user-signup'),
    # simple-jwt provides views for obtaining and refreshing tokens[cite: 141].
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]