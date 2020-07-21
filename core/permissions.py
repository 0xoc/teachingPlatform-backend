from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.translation import gettext as _

from core.models import ClassRoom, Quiz, Question, QuizAnswer
from core.utils import get_object


class IsTeacherOrSuperuser(BasePermission):
    message = _("You must be a teacher or a superuser")

    @staticmethod
    def is_teacher_or_superuser(class_id, request):
        the_class = get_object(ClassRoom, pk=class_id)

        if request.user.is_superuser:
            return True

        return the_class.teacher == request.user

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        from core.views import AddQuizQuestion
        from core.views import RUDQuestion

        if type(view) == AddQuizQuestion:
            quiz = get_object(Quiz, pk=view.kwargs.get('quiz_id'))
            class_id = quiz.class_room.id

        elif type(view) == RUDQuestion:
            question = get_object(Question, pk=view.kwargs.get('question_id'))
            quiz = question.quiz
            class_id = quiz.class_room.id
        else:
            class_id = view.kwargs.get('class_id')

        return self.is_teacher_or_superuser(class_id, request)


class IsSelfOrCanSee(BasePermission):
    message = _("You can not see details")

    def has_permission(self, request, view):
        quiz_answer = get_object(QuizAnswer, pk=view.kwargs.get('quiz_answer_id'))
        user_profile = request.user.user_profile

        class_id = quiz_answer.quiz.class_room.id

        if IsTeacherOrSuperuser.is_teacher_or_superuser(class_id, request):
            return True

        return quiz_answer.user_profile == user_profile


class IsEnrolledInClass(BasePermission):
    message = _("You are not enrolled in the class")

    @staticmethod
    def is_enrolled_in_class(class_id, request):
        the_class = get_object(ClassRoom, pk=class_id)

        return request.user.user_profile in the_class.students.all()

    def has_permission(self, request, view):

        from core.views import QuizQuestionsList, StartQuiz

        if type(view) in [QuizQuestionsList, StartQuiz]:
            quiz = get_object(Quiz, pk=view.kwargs.get('quiz_id'))
            class_id = quiz.class_room.id
        else:
            raise APIException("Invalid Permission Usage")

        return self.is_enrolled_in_class(class_id, request)


class IsQuizActive(BasePermission):
    message = _('Quiz is not active for answering')

    def has_permission(self, request, view):
        quiz = get_object(Quiz, pk=view.kwargs.get('quiz_id'))
        return quiz.is_active


class CanSeeQuizQuestions(BasePermission):
    message = _("You don't have permission to see the quiz questions")

    def has_permission(self, request, view):
        quiz = get_object(Quiz, pk=view.kwargs.get('quiz_id'))

        if IsTeacherOrSuperuser.is_teacher_or_superuser(quiz.class_room.id, request):
            return True

        if not IsEnrolledInClass.is_enrolled_in_class(quiz.class_room.id, request):
            return False

        return timezone.now() > quiz.start_datetime
