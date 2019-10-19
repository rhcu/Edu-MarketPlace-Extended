from django.db import models
from django.conf import settings
from decimal import Decimal

class Course(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    topic = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    date_created = models.DateTimeField('date published')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.0000'))

    def __str__(self):
        return self.title

ENTRIES_CHOICES = (
    ('lesson','Lesson'),
    ('video','Video'),
)

class CourseEntry(models.Model):
	name = models.CharField(max_length=500)
	entry_type = models.CharField(max_length=100, choices=ENTRIES_CHOICES, default='lesson')
	course = models.ForeignKey(Course,  on_delete=models.DO_NOTHING,)
	date_created = models.DateTimeField('date published')

class Lesson(models.Model):
	course_entry = models.ForeignKey(CourseEntry, on_delete=models.CASCADE,)
	content = models.TextField()

class Video(models.Model):
	course_entry = models.ForeignKey(CourseEntry, on_delete=models.CASCADE,)
	video_url = models.URLField(max_length=1000)
