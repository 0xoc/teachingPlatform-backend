from django.urls import path
from .views import UserProfileCreateView, ClassRoomCreateView, ClassRoomRetrieveView, QuizCreateView, RegisterQuitClass, \
    AddRemoveStudentClass

urlpatterns = [
    path('user/create', UserProfileCreateView.as_view()),

    # create retrieve class
    path('class/create/', ClassRoomCreateView.as_view()),
    path('class/<int:class_id>/', ClassRoomRetrieveView.as_view()),

    path('class/<int:class_id>/register/', RegisterQuitClass.as_view()),
    path('class/<int:class_id>/register/<int:user_id>/', AddRemoveStudentClass.as_view()),

    path('class/<int:class_id>/quiz/create/', QuizCreateView.as_view()),
]