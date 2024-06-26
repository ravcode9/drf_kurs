from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.com', password='123qwe')
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """
        Тест создания нового пользователя.

        Проверяет создание нового пользователя через API.
        """
        url = reverse('users:users-list')
        data = {
            'email': 'newuser@test.com',
            'password': 'newpassword',
            'town': 'Город',
            'is_active': True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_retrieve_user(self):
        """
        Тест получения списка пользователей.

        Проверяет получение списка всех пользователей через API.
        """
        url = reverse('users:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_user_detail(self):
        """
        Тест получения деталей пользователя.

        Проверяет получение детальной информации
         о конкретном пользователе через API.
        """
        user_id = self.user.id
        url = reverse('users:users-detail', args=[user_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')

    def test_update_user(self):
        """
        Тест обновления данных пользователя.

        Проверяет успешное обновление данных пользователя через API.
        """
        user_id = self.user.id
        url = reverse('users:users-detail', args=[user_id])
        data = {'town': 'New Town'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['town'], 'New Town')

    def test_delete_user(self):
        """
        Тест удаления пользователя.

        Проверяет успешное удаление пользователя через API.
        """
        user_id = self.user.id
        url = reverse('users:users-detail', args=[user_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_token_refresh(self):
        """
        Тест обновления токена доступа через API.

        Проверяет успешное обновление токена доступа
         с использованием refresh токена.
        """
        refresh = RefreshToken.for_user(self.user)
        url = reverse('users:token_refresh')
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
