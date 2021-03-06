# Generated by Django 3.1.1 on 2021-03-21 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.TextField()),
                ('answer', models.CharField(max_length=100)),
                ('answer_options', models.CharField(blank=True, max_length=1000, null=True)),
                ('answer_type', models.CharField(choices=[('TEXT', 'text'), ('NUMBER', 'number'), ('RADIOS', 'radios')], default='TEXT', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SolvedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.CharField(max_length=100)),
                ('right_answer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/tests/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_private', models.BooleanField(default=False)),
                ('needs_auth', models.BooleanField(default=True)),
                ('disliked_users', models.ManyToManyField(blank=True, related_name='disliked_tests', to=settings.AUTH_USER_MODEL)),
                ('liked_users', models.ManyToManyField(blank=True, related_name='liked_tests', to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(related_name='test', to='tests.Question')),
                ('tags', models.ManyToManyField(blank=True, related_name='tests', to='tags.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='SolvedTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right_answers', models.IntegerField(default=0)),
                ('date_started', models.DateTimeField()),
                ('date_ended', models.DateTimeField()),
                ('answers', models.ManyToManyField(to='tests.SolvedQuestion')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='tests.test')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solved_tests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_ended'],
            },
        ),
    ]
