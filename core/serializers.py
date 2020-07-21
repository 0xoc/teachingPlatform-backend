from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import UserProfile, ClassRoom, Quiz, Question, QuizAnswer, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.pop('user'), is_staff=True)
        _profile = UserProfile(**validated_data, user=user)
        _profile.save()

        return _profile


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'class_name', 'teacher']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'quiz_name', 'class_room']
        extra_kwargs = {
            'class_room': {'read_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text']
        extra_kwargs = {
            'quiz': {'read_only': True}
        }


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ['id', 'user_profile']


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        field = ['id', 'question', 'quiz_answer', 'answer']


class QuizRetrieveSerializer(serializers.ModelSerializer):
    answers__quiz_answer = QuizAnswerSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'questions', 'answers__quiz_answer']


class ClassRoomRetrieveSerializer(serializers.ModelSerializer):
    students = UserProfileSerializer(many=True)
    quizzes = QuizSerializer(many=True)

    class Meta:
        model = ClassRoom
        fields = ['id', 'class_name', 'teacher', 'students', 'quizzes']
