# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0019_auto_20170217_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectrequisition',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subjectrequisition',
            name='shipped_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
