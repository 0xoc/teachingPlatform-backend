from django.urls import path
from .views import UserProfileCreateView, ClassRoomCreateView, ClassRoomRetrieveView, QuizCreateView

urlpatterns = [
    path('user/create', UserProfileCreateView.as_view()),

    path('class/create', ClassRoomCreateView.as_view()),
    path('class/<int:pk>/', ClassRoomRetrieveView.as_view()),

    path('class/<int:pk>/quiz/create/', QuizCreateView.as_view()),
]