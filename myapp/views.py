from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TagEntry, PeopleCounter
from .serializers import TagEntrySerializer
from django.db.models import F
from .models import PeopleCounter  # Импортируем модель из models.py
from datetime import timedelta

# Класс для обработки POST-запросов с использованием Django REST Framework


# Класс для обработки POST-запросов с использованием Django REST Framework
class TagEntryView(APIView):
    def post(self, request):
        tag_id = request.data.get('tag_id')

        if not tag_id:
            return Response({'error': 'Tag ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, есть ли активная запись (без времени выхода) для этой метки
        active_entry = TagEntry.objects.filter(tag_id=tag_id, exit_time__isnull=True).first()

        if active_entry:
            # Обновляем время выхода и считаем общее время
            active_entry.exit_time = now()
            active_entry.total_time = active_entry.exit_time - active_entry.entry_time
            active_entry.save()
            return Response({'message': 'Exit recorded', 'total_time': active_entry.total_time}, status=status.HTTP_200_OK)
        
        # Проверяем, является ли метка новой (нет записей для данной метки)
        if not TagEntry.objects.filter(tag_id=tag_id).exists():
            # Если метка новая, создаем новую запись о входе и увеличиваем счётчик людей
            new_entry = TagEntry.objects.create(tag_id=tag_id)

            people_counter = PeopleCounter.objects.first()
            if not people_counter:
                # Если запись отсутствует, создаём её с начальным значением 0
                people_counter = PeopleCounter.objects.create(count=0)
            
            # Увеличиваем счётчик
            people_counter.count = F('count') + 1
            people_counter.save()

            # Получаем текущее количество людей
            people_count = PeopleCounter.objects.first().count
        else:
            new_entry = TagEntry.objects.create(tag_id=tag_id)
            people_count = PeopleCounter.objects.first().count

        serializer = TagEntrySerializer(new_entry)
        return Response({'entry': serializer.data, 'people_count': people_count}, status=status.HTTP_201_CREATED)




# Функция для отображения таблицы с данными из модели TagEntry
def table_view(request):
    entries = TagEntry.objects.all()  # Получаем все записи из модели TagEntry
    return render(request, 'table.html', {'entries': entries})


# Функция для отображения главной страницы
def home(request):
    return render(request, 'home.html')

# Функция для получения последней записи из модели
def get_latest_entry(request):
    try:
        latest_entry = TagEntry.objects.latest('id')
        # Проверяем, существует ли запись в PeopleCounter
        people_counter = PeopleCounter.objects.first()
        if not people_counter:
            # Если запись отсутствует, создаём её с начальным значением 0
            people_counter = PeopleCounter.objects.create(count=0)
        
        data = {
            'tag_id': latest_entry.tag_id,
            'entry_time': latest_entry.entry_time.strftime('%d/%m/%Y %H:%M:%S'),
            'exit_time': latest_entry.exit_time.strftime('%d/%m/%Y %H:%M:%S') if latest_entry.exit_time else '',
            'total_time': str(latest_entry.total_time) if latest_entry.total_time else '',
            'people_count': people_counter.count  # Получаем текущее количество людей
        }
        return JsonResponse(data)
    except TagEntry.DoesNotExist:
        return JsonResponse({'error': 'No entries found'}, status=404)
