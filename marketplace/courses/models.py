from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    topic = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    date_created = models.DateTimeField('date published')

    def __str__(self):
        return self.title
