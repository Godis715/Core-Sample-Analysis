from django.db import models
from django.contrib.auth.models import User
import uuid


class Core_sample(models.Model):
    """Основаня модель керна"""

    global_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    control_sum = models.CharField(verbose_name='Контрольная сумма', max_length=100)
    name = models.CharField(verbose_name='Название', max_length=50)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    deposit = models.PositiveIntegerField(verbose_name='Месторождение')
    hole = models.PositiveIntegerField(verbose_name='Скважина')
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    NOT_ANALYSED = 1
    ANALYSED = 2
    IN_PROCESS = 3
    ERROR = 4
    STATUS_TYPES = (
        (NOT_ANALYSED, 'notAnalysed'),
        (ANALYSED, 'analysed'),
        (IN_PROCESS, 'inProcess'),
        (ERROR, 'error'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS_TYPES, default=NOT_ANALYSED)

    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

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
    dl_density = models.FloatField(verbose_name='Плотность ДС')
    uv_density = models.FloatField(verbose_name='Плотность УФ')
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    class Meta:
        verbose_name = 'Фрагмент керна'
        verbose_name_plural = 'Фрагменты керна'

    def __str__(self):
        return str(self.id)


class Markup(models.Model):
    """Модель разметки керна"""

    cs = models.ForeignKey(Core_sample, verbose_name='Керн', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Разметка керна'
        verbose_name_plural = 'Разметки керна'

    def __str__(self):
        return str(self.id)


class Oil_layer(models.Model):
    """Модель слоя нефтенасыщенности"""

    markup = models.ForeignKey(Markup, verbose_name='Разметка', on_delete=models.CASCADE)
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    NOT_DEFINED = 1
    LOW = 2
    HIGH = 3
    CLASS_LABELS = (
        (NOT_DEFINED, 'notDefined'),
        (LOW, 'low'),
        (HIGH, 'high'),
    )
    class_label = models.IntegerField(verbose_name='Класс', choices=CLASS_LABELS)

    class Meta:
        verbose_name = 'Слой нефтенасыщенности'
        verbose_name_plural = 'Слои нефтенасыщенности'

    def __str__(self):
        return str(self.id)


class Rock_layer(models.Model):
    """Модель слоя породы"""

    markup = models.ForeignKey(Markup, verbose_name='Разметка', on_delete=models.CASCADE)
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    SILTSTONE = 1
    SANDSTONE = 2
    CLAY = 3
    CLASS_LABELS = (
        (SILTSTONE, 'siltstone'),
        (SANDSTONE, 'sandstone'),
        (CLAY, 'clay'),
    )
    class_label = models.IntegerField(verbose_name='Класс', choices=CLASS_LABELS)

    class Meta:
        verbose_name = 'Слой породы'
        verbose_name_plural = 'Слои породы'

    def __str__(self):
        return str(self.id)


class Carbon_layer(models.Model):
    """Модель слоя карбонатности"""

    markup = models.ForeignKey(Markup, verbose_name='Разметка', on_delete=models.CASCADE)
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    NOT_DEFINED = 1
    LOW = 2
    HIGH = 3
    CLASS_LABELS = (
        (NOT_DEFINED, 'notDefined'),
        (LOW, 'low'),
        (HIGH, 'high'),
    )
    class_label = models.IntegerField(verbose_name='Класс', choices=CLASS_LABELS)

    class Meta:
        verbose_name = 'Слой карбонатности'
        verbose_name_plural = 'Слои карбонатности'

    def __str__(self):
        return str(self.id)


class Disruption_layer(models.Model):
    """Модель слоя разрушенности"""

    markup = models.ForeignKey(Markup, verbose_name='Разметка', on_delete=models.CASCADE)
    top = models.FloatField(verbose_name='Вверх')
    bottom = models.FloatField(verbose_name='Низ')

    NONE = 1
    LOW = 2
    HIGH = 3
    CLASS_LABELS = (
        (NONE, 'none'),
        (LOW, 'low'),
        (HIGH, 'high'),
    )
    class_label = models.IntegerField(verbose_name='Класс', choices=CLASS_LABELS)

    class Meta:
        verbose_name = 'Слой разрушенности'
        verbose_name_plural = 'Слои разрушенности'

    def __str__(self):
        return str(self.id)
