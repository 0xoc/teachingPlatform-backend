from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from core.models import ClassRoom
from core.permissions import IsTeacherOrSuperuser
from core.serializers import UserProfileSerializer, ClassRoomCreateSerializer, ClassRoomRetrieveSerializer, \
    QuizSerializer


class UserProfileCreateView(CreateAPIView):
    """
    create user profile
    """
    serializer_class = UserProfileSerializer


class ClassRoomCreateView(CreateAPIView):
    """
    create class room
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClassRoomCreateSerializer


class QuizCreateView(CreateAPIView):
    """
    Create quiz for a class, only class teacher and supers users
    """
    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser, ]
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        _class = get_object_or_404(ClassRoom, pk=self.kwargs.get('pk'))
        serializer.save(class_room=_class)


class ClassRoomRetrieveView(RetrieveAPIView):
    """
    retrieve class room, list of students and quizzes will be returned
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClassRoomRetrieveSerializer
    queryset = ClassRoom.objects.all()
