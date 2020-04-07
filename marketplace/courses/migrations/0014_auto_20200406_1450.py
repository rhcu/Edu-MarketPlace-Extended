# Generated by Django 2.2.5 on 2020-04-06 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20200406_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='file',
            field=models.FileField(blank=True, upload_to='assignments/'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='student',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]