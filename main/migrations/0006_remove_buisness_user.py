# Generated by Django 3.0.2 on 2021-02-20 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_buisness_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buisness',
            name='user',
        ),
    ]
