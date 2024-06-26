from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'place')
    search_fields = ('user', 'action', 'place')
    list_filter = ('user', 'action')
