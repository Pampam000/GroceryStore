from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from applications.users.api.serializers import UserSerializer
from applications.users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
