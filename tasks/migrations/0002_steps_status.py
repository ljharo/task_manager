# Generated by Django 5.0.6 on 2024-06-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='steps',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
