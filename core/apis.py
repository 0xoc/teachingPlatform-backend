from django.urls import path
from .views import UserProfileCreateView


urlpatterns = [
    path('user/create', UserProfileCreateView.as_view()),
]