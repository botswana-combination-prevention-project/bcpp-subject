# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-16 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0013_auto_20170216_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectrequisition',
            name='slug',
            field=models.CharField(db_index=True, editable=False, help_text='a field used for quick search', max_length=250, null=True),
        ),
    ]
