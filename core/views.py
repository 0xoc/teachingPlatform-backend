from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from core.serializers import UserProfileSerializer, ClassRoomCreateSerializer, ClassRoomRetrieveSerializer


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileSerializer


class ClassRoomCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClassRoomCreateSerializer


class ClassRoomRetrieve(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClassRoomRetrieveSerializer

