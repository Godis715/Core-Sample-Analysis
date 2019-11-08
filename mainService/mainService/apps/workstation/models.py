from django.db import models
from django.contrib.auth.models import User


class Workstation(models.Model):
    """Модель рабочего окружения"""

    title = models.CharField(verbose_name='Название', max_length=50, null=True)
    description = models.TextField(verbose_name='Описание', max_length=200, null=True)
    creator = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE, default=None)
    invited = models.ManyToManyField(User, verbose_name='Участники', related_name='invited_worker')
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Рабочие окружение'
        verbose_name_plural = 'Рабочие окружения'

    def __str__(self):
        return self.title
