# Generated by Django 2.2.5 on 2019-10-19 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_merge_20191019_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseentry',
            name='entry_type',
            field=models.CharField(choices=[('lesson', 'Lesson'), ('video', 'Video')], default='lesson', max_length=100),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField(max_length=1000)),
                ('course_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseEntry')),
            ],
        ),
    ]
