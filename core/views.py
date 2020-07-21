from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, \
    RetrieveUpdateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ClassRoom, UserProfile, Quiz, Question
from core.permissions import IsTeacherOrSuperuser, CanSeeQuizQuestions, IsEnrolledInClass, IsQuizActive
from core.serializers import UserProfileSerializer, ClassRoomSerializer, ClassRoomRetrieveSerializer, \
    QuizSerializer, QuestionSerializer, QuizAnswerSerializer
from core.utils import get_object


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
    serializer_class = ClassRoomSerializer


class QuizCreateView(CreateAPIView):
    """
    Create quiz for a class, only class teacher and supers users
    """
    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser, ]
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        _class = get_object(ClassRoom, pk=self.kwargs.get('class_id'))
        serializer.save(class_room=_class)


class AddQuizQuestion(CreateAPIView):
    """
    Add question to quiz, only class teacher and superusers
    """
    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser]

    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        quiz = get_object(Quiz, pk=self.kwargs.get('quiz_id'))
        serializer.save(quiz=quiz)


class RUDQuestion(RetrieveUpdateDestroyAPIView):
    """
    Retrieve update delete quiz question
    """

    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'question_id'


class QuizQuestionsList(ListAPIView):
    """
    get quiz questions
    teachers and super users can always see questions
    otherwise only enrolled students after quiz started
    """
    permission_classes = [IsAuthenticated, CanSeeQuizQuestions]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz = get_object(Quiz, pk=self.kwargs.get('quiz_id'))
        return quiz.questions.all()


class StartQuiz(CreateAPIView):
    """
    Start quiz answering session
    """
    permission_classes = [IsAuthenticated, IsEnrolledInClass, IsQuizActive]
    serializer_class = QuizAnswerSerializer

    def perform_create(self, serializer):
        quiz = get_object(Quiz, pk=self.kwargs.get('quiz_id'))
        serializer.save(quiz=quiz)


class RegisterQuitClass(APIView):
    """
    currently logged in user will be registered to the given class if method is post
    and will be removed from class if method is delete
    """
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def post(request, *args, **kwargs):
        user_profile = request.user.user_profile
        _class = get_object(ClassRoom, pk=kwargs.get('class_id'))
        _class.students.add(user_profile)

        return Response({}, status=200)

    @staticmethod
    def delete(request, *args, **kwargs):
        user_profile = request.user.user_profile
        _class = get_object(ClassRoom, pk=kwargs.get('class_id'))
        _class.students.remove(user_profile)

        return Response({}, status=204)


class AddRemoveStudentClass(APIView):
    """
    add/remove a given student to the give class
    only class teacher and superuser
    """
    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser]

    @staticmethod
    def post(request, *args, **kwargs):
        user_profile = get_object(UserProfile, pk=kwargs.get('user_id'))
        class_room = get_object(ClassRoom, pk=kwargs.get('class_id'))

        class_room.students.add(user_profile)

        return Response({}, status=200)

    @staticmethod
    def delete(request, *args, **kwargs):
        user_profile = get_object(UserProfile, pk=kwargs.get('user_id'))
        class_room = get_object(ClassRoom, pk=kwargs.get('class_id'))

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


class ClassRoomUpdateView(RetrieveUpdateAPIView):
    """
    Retrieve update class info
    """
    permission_classes = [IsAuthenticated, IsTeacherOrSuperuser]
    serializer_class = ClassRoomSerializer
    queryset = ClassRoom.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'class_id'
