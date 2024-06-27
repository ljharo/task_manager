# Generated by Django 5.0.6 on 2024-06-24 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=10, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'status',
                'db_table': 'task_status',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('id_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.status')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='Steps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('id_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
            options={
                'verbose_name': 'task_steps',
                'verbose_name_plural': 'task_steps',
                'db_table': 'task_steps',
            },
        ),
    ]