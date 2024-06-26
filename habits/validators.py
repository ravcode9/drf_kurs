from django.core.exceptions import ValidationError


def validate_no_reward_and_related_habit(reward, related_habit):
    if reward and related_habit:
        raise ValidationError('Нельзя одновременно'
                              ' указать связанную привычку и вознаграждение.')


def validate_duration(duration):
    if duration > 120:
        raise ValidationError('Время на выполнение'
                              ' не может превышать 120 секунд.')


def validate_periodicity(periodicity):
    if periodicity > 7:
        raise ValidationError('Периодичность не может превышать 7 дней.')


def validate_related_habit_is_pleasant(related_habit):
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError('Связанной привычкой может быть'
                              ' только привычка'
                              ' с признаком приятной привычки.')


def validate_pleasant_habit(reward, related_habit, is_pleasant):
    if is_pleasant and (reward or related_habit):
        raise ValidationError('У приятной привычки не может'
                              ' быть вознаграждения или связанной привычки.')
