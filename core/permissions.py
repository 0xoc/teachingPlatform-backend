from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.translation import gettext as _

from core.models import ClassRoom, Quiz


class IsTeacherOrSuperuser(BasePermission):
    message = _("You must be a teacher or a superuser")

    @staticmethod
    def is_teacher_or_superuser(class_id, request):
        the_class = get_object_or_404(ClassRoom, pk=class_id)

        if request.user.is_superuser:
            return True

        return the_class.teacher == request.user

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return self.is_teacher_or_superuser(view.kwargs.get('class_id'), request)


class IsEnrolledInClass(BasePermission):
    message = _("You are not enrolled in the class")

    @staticmethod
    def is_enrolled_in_class(class_id, request):
        the_class = get_object_or_404(ClassRoom, pk=class_id)

        return request.user.user_profile in the_class.students.all()

    def has_permission(self, request, view):

        from core.views import QuizQuestionsList

        if type(view) == QuizQuestionsList:
            quiz = get_object_or_404(Quiz, pk=view.kwargs.get('quiz_id'))
            class_id = quiz.class_room.id
        else:
            raise APIException("Invalid Permission Usage")

        return self.is_enrolled_in_class(class_id, request)


class CanSeeQuizQuestions(BasePermission):
    message = _("You don't have permission to see the quiz questions")

    def has_permission(self, request, view):
        quiz = get_object_or_404(Quiz, pk=view.kwargs.get('quiz_id'))

        if IsTeacherOrSuperuser.is_teacher_or_superuser(quiz.class_room.id, request):
            return True

        if not IsEnrolledInClass.is_enrolled_in_class(quiz.class_room.id, request):
            return False

        return quiz.start_datetime > timezone.now()
