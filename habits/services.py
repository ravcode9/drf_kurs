import requests
from config import settings


# def set_schedule(*args, **kwargs):
#     schedule, created = IntervalSchedule.objects.get_or_create(
#         every=2,
#         period=IntervalSchedule.HOURS,
#     )
#     PeriodicTask.objects.create(
#         interval=schedule,
#         name='send_habit_reminders',
#         task='habits.tasks.send_habit_reminders',
#         kwargs=json.dumps({
#             'be_careful': True,
#         }),
#         expires=datetime.utcnow() + timedelta(seconds=30)
#     )


def send_telegram_message(chat_id, message):
    params = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(f'{settings.TELEGRAM_URL}'
                                 f'{settings.TELEGRAM_TOKEN}'
                                 f'/sendMessage', params=params)
        response.raise_for_status()
        print(f"Сообщение успешно отправлено: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки сообщения: {e}, Response:"
              f" {response.text if response else 'Нет ответа'}")
        return None
