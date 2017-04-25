# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 20:59
from __future__ import unicode_literals

from django.db import migrations
import edc_base.model_fields.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0035_auto_20170316_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpimacd4',
            name='reason_not_done_other',
            field=edc_base.model_fields.custom_fields.OtherCharField(blank=True, editable=True, max_length=50, verbose_name='...if "Other", specify'),
        ),
        migrations.AlterField(
            model_name='historicalpimavl',
            name='reason_not_done_other',
            field=edc_base.model_fields.custom_fields.OtherCharField(blank=True, editable=True, max_length=50, verbose_name='...if "Other", specify'),
        ),
        migrations.AlterField(
            model_name='pimacd4',
            name='reason_not_done_other',
            field=edc_base.model_fields.custom_fields.OtherCharField(blank=True, editable=True, max_length=50, verbose_name='...if "Other", specify'),
        ),
        migrations.AlterField(
            model_name='pimavl',
            name='reason_not_done_other',
            field=edc_base.model_fields.custom_fields.OtherCharField(blank=True, editable=True, max_length=50, verbose_name='...if "Other", specify'),
        ),
    ]