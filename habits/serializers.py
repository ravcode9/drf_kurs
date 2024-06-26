from rest_framework import serializers
from .models import Habit
from users.serializers import UserSerializer


class HabitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'


class PublicHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'action',
                  'time', 'place', 'is_pleasant', 'duration', 'periodicity']
