from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.models import ClassRoom


class IsTeacherOrSuperuser(BasePermission):

    def has_permission(self, request, view):

        from core.views import QuizCreateView
        from core.views import AddStudentToClass

        if request.method in SAFE_METHODS:
            return True

        the_class = get_object_or_404(ClassRoom, pk=view.kwargs.get('class_id'))

        if request.user.is_superuser:
            return True

        return the_class.teacher == request.user
