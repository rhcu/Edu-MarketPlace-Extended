# Generated by Django 3.0.2 on 2020-02-02 18:52

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_useranswer_userquizpassed'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0000'), max_digits=9),
        ),
        migrations.AddField(
            model_name='courseenroll',
            name='user_rating',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0000'), max_digits=9),
        ),
    ]
