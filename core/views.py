from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from core.serializers import UserProfileCreateSerializer, ClassRoomSerializer


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer


class ClassRoomCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClassRoomSerializer

