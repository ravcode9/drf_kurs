from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from habits.models import Habit
from django.core.exceptions import ValidationError
from habits.validators import (
    validate_no_reward_and_related_habit,
    validate_duration,
    validate_periodicity,
    validate_related_habit_is_pleasant,
    validate_pleasant_habit,
)

User = get_user_model()


class HabitCRUDTestCase(APITestCase):
    """
    Тесты для создания, чтения, обновления и удаления привычек.
    """

    def setUp(self):
        """
        Настройка данных для тестов.
        """
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.com', password='123qwe')
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            action='Бегать',
            time='07:00:00',
            place='Парк',
            is_pleasant=True,
            duration=100,
            periodicity=1,
        )

    def test_create_habit(self):
        """
        Тест создания новой привычки.
        """
        data = {
            'action': 'Прогулка',
            'time': '08:00:00',
            'place': 'Парк',
            'is_pleasant': True,
            'duration': 120,
            'periodicity': 2
        }
        response = self.client.post(reverse('habits:habit-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Прогулка')

    def test_read_habit(self):
        """
        Тест чтения существующей привычки.
        """
        response = self.client.get(reverse('habits:habit-detail',
                                           args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Бегать')

    def test_update_habit(self):
        """
        Тест обновления существующей привычки.
        """
        data = {
            'action': 'Бег',
        }
        response = self.client.patch(reverse(
            'habits:habit-detail', args=[self.habit.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Бег')

    def test_delete_habit(self):
        """
        Тест удаления существующей привычки.
        """
        response = self.client.delete(reverse(
            'habits:habit-detail', args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_validate_no_reward_and_related_habit(self):
        """
        Тест валидатора validate_no_reward_and_related_habit.
        """
        validate_no_reward_and_related_habit(None, None)

        with self.assertRaises(ValidationError):
            validate_no_reward_and_related_habit('Награда', Habit())

    def test_validate_duration(self):
        """
        Тест валидатора validate_duration.
        """
        validate_duration(100)

        with self.assertRaises(ValidationError):
            validate_duration(300)

    def test_validate_periodicity(self):
        """
        Тест валидатора validate_periodicity.
        """
        validate_periodicity(1)

        with self.assertRaises(ValidationError):
            validate_periodicity(8)

    def test_validate_related_habit_is_pleasant(self):
        """
        Тест валидатора validate_related_habit_is_pleasant.
        """
        habit = Habit.objects.create(
            user=self.user,
            action='Упражняться',
            time='07:00:00',
            place='Спортзал',
            is_pleasant=True,
            duration=120,
            periodicity=1,
        )
        validate_related_habit_is_pleasant(habit)

        habit.is_pleasant = False
        habit.save()
        with self.assertRaises(ValidationError):
            validate_related_habit_is_pleasant(habit)

    def test_validate_pleasant_habit(self):
        """
        Тест валидатора validate_pleasant_habit.
        """
        validate_pleasant_habit(None, None, True)

        with self.assertRaises(ValidationError):
            validate_pleasant_habit('Награда', None, True)
