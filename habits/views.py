from rest_framework import viewsets
from users.permissions import IsOwner
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления привычками пользователя.

    Атрибуты:
        serializer_class (HabitSerializer): Сериализатор для модели Habit.
        permission_classes (list): Список классов разрешений по умолчанию.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получение QuerySet для текущего запроса.

        Если запрос исходит от суперпользователя, возвращаются все привычки.
        В противном случае возвращаются только привычки текущего пользователя.

        Возвращает:
            QuerySet: QuerySet объектов Habit.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Habit.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Сохранение нового объекта Habit с привязкой к текущему пользователю.

        Аргументы:
            serializer (HabitSerializer): Сериализатор объекта Habit.
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Получение списка разрешений для текущего действия.

        Определяет список разрешений на основе текущего действия (action).
        Разрешения на действия 'update', 'partial_update'
         и 'destroy' требуют проверки владельца (IsOwner).
        Действие 'public_habits' доступно всем (AllowAny).
        Все остальные действия требуют аутентификации (IsAuthenticated).

        Возвращает:
            list: Список разрешений для текущего действия.
        """
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'public_habits':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
