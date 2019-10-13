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
