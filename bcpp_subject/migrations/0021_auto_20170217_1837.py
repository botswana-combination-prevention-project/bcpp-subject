# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0020_auto_20170217_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectrequisition',
            name='specimen_identifier',
        ),
        migrations.AddField(
            model_name='subjectrequisition',
            name='identifier_prefix',
            field=models.CharField(editable=False, max_length=50, null=True, unique=True),
        ),
    ]
