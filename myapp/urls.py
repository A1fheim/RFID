from django.urls import path
from . import views
from .views import TagEntryView

urlpatterns = [
    path('table/', views.table_view, name='table_view'),
    path('tag-entry/', views.TagEntryView.as_view(), name='tag_entry'),
    path('', views.home, name='home'),  # Главная страница
    path('get-latest-entry/', views.get_latest_entry, name='get_latest_entry'),
    path('api/rfid/', TagEntryView.as_view(), name='rfid_entry'),  # Только один маршрут для API
    path('table/', views.table_view, name='table_view'),
]
