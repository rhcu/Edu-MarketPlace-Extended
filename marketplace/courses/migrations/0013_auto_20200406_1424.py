# Generated by Django 2.2.5 on 2020-04-06 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0012_auto_20200202_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseentry',
            name='entry_type',
            field=models.CharField(choices=[('lesson', 'Lesson'), ('video', 'Video'), ('quiz', 'Quiz'), ('assignment', 'Assignment')], default='lesson', max_length=100),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='assignments/')),
                ('course_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseEntry')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]