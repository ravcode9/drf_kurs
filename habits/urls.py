from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import HabitsConfig
from .views import HabitViewSet

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', HabitViewSet.as_view({'get': 'public_habits'}), name='public-habits'),
]
