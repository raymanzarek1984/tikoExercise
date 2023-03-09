from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer
