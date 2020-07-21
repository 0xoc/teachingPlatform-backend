from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)


class ClassRoom(models.Model):
    class_name = models.CharField(max_length=255)
    teacher = models.ForeignKey(UserProfile, related_name='classes', on_delete=models.CASCADE)


class Quiz(models.Model):
    class_room = models.ForeignKey(ClassRoom, related_name="quizzes", on_delete=models.CASCADE)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    quiz_answer = models.ForeignKey("QuizAnswer", related_name="answers", on_delete=models.CASCADE)
    answer = models.TextField()


class QuizAnswer(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name="quiz_answers", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
