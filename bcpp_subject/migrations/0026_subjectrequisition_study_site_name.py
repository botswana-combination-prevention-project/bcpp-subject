# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-28 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0025_auto_20170223_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectrequisition',
            name='study_site_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
