# Generated by Django 3.1.1 on 2020-10-29 11:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_liked_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 29, 11, 35, 28, 548917, tzinfo=utc)),
        ),
    ]
