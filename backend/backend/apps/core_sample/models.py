from django.db import models
from django.contrib.auth.models import User
import uuid


class Core_sample(models.Model):
    """Основаня модель керна"""

    global_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Название', max_length=50)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    deposit = models.PositiveIntegerField(verbose_name='Месторождение')
    hole = models.PositiveIntegerField(verbose_name='Скважина')
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    NOT_ANALYSED = 1
    ANALYSED = 2
    IN_PROGRESS = 3
    ERROR = 4
    STATUS_TYPES = (
        (NOT_ANALYSED, 'notAnalysed'),
        (ANALYSED, 'analysed'),
        (IN_PROGRESS, 'inProcess'),
        (ERROR, 'error'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS_TYPES, default=NOT_ANALYSED)

    class Meta:
        verbose_name = 'Керн'
        verbose_name_plural = 'Керны'

    def __str__(self):
        return self.name


class Fragment(models.Model):
    """Модель фрагмента керна"""

    cs = models.ForeignKey(Core_sample, verbose_name='Керн', on_delete=models.CASCADE)
    dl_src = models.FilePathField(verbose_name='ДС изображение')
    uv_src = models.FilePathField(verbose_name='УФ изображение')
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    class Meta:
        verbose_name = 'Фрагмент керна'
        verbose_name_plural = 'Фрагменты керна'

    def __str__(self):
        return str(self.id)
