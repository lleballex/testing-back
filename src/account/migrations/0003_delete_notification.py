# Generated by Django 3.1.1 on 2021-03-22 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_notification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]