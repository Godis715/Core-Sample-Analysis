# Generated by Django 2.2.6 on 2019-10-25 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_sample', '0013_auto_20191025_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fragment',
            old_name='dl_density',
            new_name='dl_resolution',
        ),
        migrations.RenameField(
            model_name='fragment',
            old_name='uv_density',
            new_name='uv_resolution',
        ),
    ]
