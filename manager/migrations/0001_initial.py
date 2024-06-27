# Generated by Django 5.0.6 on 2024-06-24 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_ip', models.CharField(max_length=20, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'address_ip',
                'verbose_name_plural': 'address_ips',
                'db_table': 'manager_address_ip',
            },
        ),
        migrations.CreateModel(
            name='RestAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=10)),
                ('status', models.BooleanField()),
            ],
            options={
                'verbose_name': 'rest_action',
                'verbose_name_plural': 'rest_actions',
                'db_table': 'manager_rest_action',
            },
        ),
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
                'db_table': 'manager_status',
            },
        ),
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('endpoint', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('action_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manager.restaction')),
            ],
            options={
                'verbose_name': 'api',
                'verbose_name_plural': 'apis',
                'db_table': 'manager_api',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_date', models.DateTimeField(auto_now=True)),
                ('addres_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manager.addressip')),
                ('api_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manager.api')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manager.status')),
            ],
            options={
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
                'db_table': 'manager_log',
            },
        ),
    ]