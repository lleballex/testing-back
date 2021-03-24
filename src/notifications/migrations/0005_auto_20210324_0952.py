# Generated by Django 3.1.1 on 2021-03-24 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20210324_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='kind',
            field=models.CharField(choices=[('GREETING', 'greeting'), ('NEW_USER', 'new user'), ('NEW_TEST', 'new test'), ('NEW_SOLUTION', 'new solution')], max_length=12),
        ),
    ]