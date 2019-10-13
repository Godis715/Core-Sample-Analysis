# Generated by Django 2.2.6 on 2019-10-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_sample', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='core_sample',
            name='bottom',
            field=models.FloatField(verbose_name='Низ'),
        ),
        migrations.AlterField(
            model_name='core_sample',
            name='deposit',
            field=models.IntegerField(verbose_name='Месторождение'),
        ),
        migrations.AlterField(
            model_name='core_sample',
            name='hole',
            field=models.IntegerField(verbose_name='Скважина'),
        ),
        migrations.AlterField(
            model_name='core_sample',
            name='top',
            field=models.FloatField(verbose_name='Вверх'),
        ),
    ]
