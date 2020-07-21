from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ClassRoom, UserProfile
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
        _class = get_object_or_404(ClassRoom, pk=self.kwargs.get('class_id'))
        serializer.save(class_room=_class)


class RegisterQuitClass(APIView):
    """
    currently logged in user will be registered to the given class if method is post
    and will be removed from class if method is delete
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.user_profile
        _class = get_object_or_404(ClassRoom, pk=kwargs.get('class_id'))
        _class.students.add(user_profile)

        return Response({}, status=200)

    def delete(self, request, *args, **kwargs):
        user_profile = request.user.user_profile
        _class = get_object_or_404(ClassRoom, pk=kwargs.get('class_id'))
        _class.students.remove(user_profile)

        return Response({}, status=204)


class AddRemoveStudentClass(APIView):
    """
    add/remove a given student to the give class
    only class teacher and superuser
    """
    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser]

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, pk=kwargs.get('user_id'))
        class_room = get_object_or_404(ClassRoom, pk=kwargs.get('class_id'))

        class_room.students.add(user_profile)

        return Response({}, status=200)

    def delete(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, pk=kwargs.get('user_id'))
        class_room = get_object_or_404(ClassRoom, pk=kwargs.get('class_id'))

        class_room.students.remove(user_profile)

        return Response({}, status=204)


class ClassRoomRetrieveView(RetrieveAPIView):
    """
    retrieve class room, list of students and quizzes will be returned
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClassRoomRetrieveSerializer
    queryset = ClassRoom.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'class_id'
