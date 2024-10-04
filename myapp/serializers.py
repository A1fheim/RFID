from rest_framework import serializers
from .models import TagEntry

class TagEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagEntry
        fields = '__all__'  # Если хочешь все поля, либо можешь выбрать только нужные
