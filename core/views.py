from rest_framework.generics import CreateAPIView

from core.serializers import UserProfileCreateSerializer


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer

