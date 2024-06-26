from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    APIView для регистрации нового пользователя.

    Атрибуты:
        queryset: QuerySet для всех объектов пользователя.
        permission_classes: Разрешения для доступа к этому представлению.
        serializer_class: Класс сериализатора для объекта пользователя.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Создает нового пользователя и генерирует токены JWT.

        Аргументы:
            serializer: Сериализатор с данными пользователя.

        Возвращает:
            Response: Ответ с токенами доступа и обновления.
        """
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.

    Атрибуты:
        serializer_class: Класс сериализатора для объекта пользователя.
        queryset: QuerySet для всех объектов пользователя.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
