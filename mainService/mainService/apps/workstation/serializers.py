from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Workstation


class WorkerSerializer(serializers.ModelSerializer):
    """Сериализация сотрудника"""
    class Meta:
        model = User
        fields = ('id', 'username')


class WorkstationSerializer(serializers.ModelSerializer):
    """Сериализация рабочего окружения"""

    creator = WorkerSerializer()
    invited = WorkerSerializer(many=True)

    class Meta:
        model = Workstation
        fields = ('title', 'description', 'creator', 'invited', 'date')
