# Generated by Django 3.1.1 on 2020-10-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_auto_20201018_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='tags',
            field=models.ManyToManyField(related_name='tests', to='tests.Tag'),
        ),
    ]