# Generated by Django 2.2.5 on 2019-11-12 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0009_auto_20191110_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProgression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('course_entry', models.ForeignKey(limit_choices_to={'course': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')}, on_delete=django.db.models.deletion.CASCADE, to='courses.CourseEntry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
