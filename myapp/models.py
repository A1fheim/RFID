from django.db import models

class TagEntry(models.Model):
    tag_id = models.CharField(max_length=100)  # ID метки
    entry_time = models.DateTimeField(auto_now_add=True)  # Время входа
    exit_time = models.DateTimeField(null=True, blank=True)  # Время выхода
    total_time = models.DurationField(null=True, blank=True)  # Суммарное время пребывания

    def __str__(self):
        return f"Tag ID: {self.tag_id}, Entry: {self.entry_time}, Exit: {self.exit_time}"

# Модель для хранения количества людей
class PeopleCounter(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Количество людей: {self.count}"