from datetime import timedelta
from celery import shared_task
from django.utils import timezone
import pytz
from .models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.now()
    almaty_now = now.astimezone(pytz.timezone('Asia/Almaty'))

    start_time = (almaty_now - timedelta(minutes=1)).time()
    end_time = (almaty_now + timedelta(minutes=1)).time()

    habits = Habit.objects.filter(time__gte=start_time, time__lte=end_time)

    if not habits:
        print("Нету привычек для отправки уведомлений на данный момент")
    else:
        for habit in habits:
            print(f"Отправка уведомления о привычке: {habit.action}")
            if habit.user.chat_id:
                send_telegram_message(
                    habit.user.chat_id, f'Уведомление о привычке:'
                                        f' {habit.action} {habit.place}')
            else:
                print(f"У пользователя"
                      f" {habit.user} не указан chat_id")
