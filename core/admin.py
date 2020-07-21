from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']

    @staticmethod
    def username(up):
        return up.user.username

    @staticmethod
    def first_name(up):
        return up.user.first_name

    @staticmethod
    def last_name(up):
        return up.user.last_name


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_name', 'start_datetime', 'end_datetime', 'is_active', 'class_room']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'quiz', 'quiz_id', 'class_id']

    @staticmethod
    def quiz_id(q):
        return q.quiz.id

    @staticmethod
    def class_id(q):
        return q.quiz.class_room.id


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ClassRoom)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuizAnswer)
