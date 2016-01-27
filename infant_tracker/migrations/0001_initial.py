# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_type', models.CharField(choices=[('WK', 'Woke'), ('NRS', 'Nursed'), ('NPD', 'Napped'), ('BTL', 'Bottle'), ('ACT', 'Activity'), ('BDTM', 'Bedtime'), (None, '-----------')], max_length=2, verbose_name='What Happened')),
                ('event_notes', models.TextField(verbose_name='Event Notes')),
            ],
        ),
    ]
