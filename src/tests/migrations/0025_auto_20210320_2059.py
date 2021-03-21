# Generated by Django 3.1.1 on 2021-03-20 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0024_auto_20210320_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvedtest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='tests.test'),
        ),
        migrations.AlterField(
            model_name='solvedtest',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='solved_tests', to=settings.AUTH_USER_MODEL),
        ),
    ]
