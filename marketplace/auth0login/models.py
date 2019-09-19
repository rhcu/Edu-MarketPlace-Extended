from django.db import models

# Create your models here.
class UserData(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    picture = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    date = models.DateTimeField('date published')