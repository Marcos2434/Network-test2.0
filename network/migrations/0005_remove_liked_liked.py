# Generated by Django 3.1.1 on 2020-10-29 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20201029_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liked',
            name='liked',
        ),
    ]
