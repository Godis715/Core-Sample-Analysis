# Generated by Django 2.2.6 on 2019-10-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_sample', '0004_fragment_density'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fragment',
            name='density',
        ),
        migrations.AddField(
            model_name='fragment',
            name='dl_density',
            field=models.FloatField(default=100.0, verbose_name='Плотность ДС'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fragment',
            name='uv_density',
            field=models.FloatField(default=100.0, verbose_name='Плотность УФ'),
            preserve_default=False,
        ),
    ]
