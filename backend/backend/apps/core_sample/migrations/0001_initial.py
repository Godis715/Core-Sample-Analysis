# Generated by Django 2.2.6 on 2019-10-13 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Core_sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.CharField(max_length=50, verbose_name='Месторождение')),
                ('hole', models.CharField(max_length=50, verbose_name='Скважина')),
                ('top', models.CharField(max_length=50, verbose_name='Вверх')),
                ('bottom', models.CharField(max_length=50, verbose_name='Низ')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Образец керна',
                'verbose_name_plural': 'Образцы керна',
            },
        ),
    ]
