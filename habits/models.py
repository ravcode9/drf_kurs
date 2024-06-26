from django.db import models
from habits.validators import (validate_no_reward_and_related_habit,
                               validate_duration,
                               validate_periodicity,
                               validate_related_habit_is_pleasant,
                               validate_pleasant_habit)


class Habit(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             verbose_name="Пользователь")
    action = models.CharField(max_length=255,
                              verbose_name="Действие")
    time = models.TimeField(verbose_name="Время")
    place = models.CharField(max_length=255, verbose_name="Место")
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name="Приятная привычка")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      verbose_name="Связанная привычка")
    reward = models.CharField(max_length=255, null=True, blank=True,
                              verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(
        verbose_name="Время на выполнение (сек.)")
    is_public = models.BooleanField(default=False,
                                    verbose_name="Публичная привычка")
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дни)")

    def clean(self):
        validate_no_reward_and_related_habit(self.reward, self.related_habit)
        validate_duration(self.duration)
        validate_periodicity(self.periodicity)
        validate_related_habit_is_pleasant(self.related_habit)
        validate_pleasant_habit(
            self.reward, self.related_habit, self.is_pleasant)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.time}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
