# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0003_auto_20170915_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchedelement',
            name='check_interval_hours',
            field=models.FloatField(default=1.0, help_text='The interval to check html element in hours.'),
        ),
        migrations.AlterField(
            model_name='watchedelement',
            name='html_element',
            field=models.CharField(help_text='Css selector for the element to watch.', max_length=200),
        ),
    ]
