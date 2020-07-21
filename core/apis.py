from django.urls import path
from .views import UserProfileCreateView, ClassRoomCreateView

urlpatterns = [
    path('user/create', UserProfileCreateView.as_view()),
    path('class/create', ClassRoomCreateView.as_view()),

]