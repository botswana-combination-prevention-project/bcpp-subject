# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-26 08:34
from __future__ import unicode_literals

import _socket
from django.db import migrations, models
import django_revision.revision_field
import edc_base.model_fields.hostname_modification_field
import edc_base.model_fields.userfield
import edc_base.model_fields.uuid_auto_field
import edc_base.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0042_auto_20180126_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationPrescribed',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, help_text='(suggest 40 characters max.)', max_length=250, unique=True, verbose_name='Name')),
                ('short_name', models.CharField(db_index=True, help_text='This is the stored value, required', max_length=250, unique=True, verbose_name='Stored value')),
                ('display_index', models.IntegerField(db_index=True, default=0, help_text='Index to control display order if not alphabetical, not required', verbose_name='display index')),
                ('field_name', models.CharField(blank=True, editable=False, help_text='Not required', max_length=25, null=True)),
                ('version', models.CharField(default='1.0', editable=False, max_length=35)),
            ],
            options={
                'verbose_name_plural': 'Medication Prescribed',
                'ordering': ['display_index', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestsOrdered',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, help_text='(suggest 40 characters max.)', max_length=250, unique=True, verbose_name='Name')),
                ('short_name', models.CharField(db_index=True, help_text='This is the stored value, required', max_length=250, unique=True, verbose_name='Stored value')),
                ('display_index', models.IntegerField(db_index=True, default=0, help_text='Index to control display order if not alphabetical, not required', verbose_name='display index')),
                ('field_name', models.CharField(blank=True, editable=False, help_text='Not required', max_length=25, null=True)),
                ('version', models.CharField(default='1.0', editable=False, max_length=35)),
            ],
            options={
                'verbose_name_plural': 'Tests Ordered',
                'ordering': ['display_index', 'name'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='cancer_care',
            field=models.IntegerField(verbose_name='Of the times you sought care, how many times were you seekingcare for Cancer diagnosis, treatment?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='chronic_disease',
            field=models.IntegerField(help_text='Chronic disease-related care(e.g high blood pressure,diabetes, depression', verbose_name='Of the times you sought care, how many times were you seekingcare for Chronic disease-related care?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='further_evaluation',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], max_length=3, verbose_name='For the most recent time that you sought care, were you referred for further evaluation or treatment?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='hiv_related',
            field=models.IntegerField(help_text='(such as ART start, refill,routinemonitoring', verbose_name='Of the times you sought care, how many times were you seeking care for Routine HIV-related care?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='hiv_related_none_tb',
            field=models.IntegerField(verbose_name='Of the times you sought care, how many times were you seeking Diagnosis or Treatment of HIV-related illness other than?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='injury_accident',
            field=models.IntegerField(verbose_name='Of the times you sought care, how many times were you seekingcare for Injury or Accident?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='lab_tests_ordered',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer"), ('cant_remember', 'Cannot remember')], max_length=3, verbose_name='For the most recent time that you sought care, were any labtests ordered?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='medication',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], max_length=6, verbose_name='For the most recent time that you sought care, wereany medications prescribed?'),
        ),
        migrations.RemoveField(
            model_name='ceaopd',
            name='medication_prescribed',
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='pregnancy_related',
            field=models.IntegerField(help_text='Pregnancy related care (e.g. antenatal, postnatal care', verbose_name='Of the times you sought care, how many times were you seeking care for Pregnancy related care?'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='procedure',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='If yes, describe:'),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='procedures_performed',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer"), ('cant_remember', 'Cannot remember')], max_length=3, verbose_name=' For the most recent time that you sought care, wereany procedures performed? '),
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='tb_care',
            field=models.IntegerField(verbose_name='Of the times you sought care, how many times were you seeking care for TB Diagnosis or Treatment?'),
        ),
        migrations.RemoveField(
            model_name='ceaopd',
            name='tests_ordered',
        ),
        migrations.AlterField(
            model_name='ceaopd',
            name='times_care_obtained',
            field=models.IntegerField(verbose_name='Of the times you sought care, how many times were you able to obtain care?'),
        ),
        migrations.AddField(
            model_name='ceaopd',
            name='medication_prescribed',
            field=models.ManyToManyField(blank=True, related_name='medication_prescribed', to='bcpp_subject.MedicationPrescribed', verbose_name='If yes,indicate which of the following were prescribed.'),
        ),
        migrations.AddField(
            model_name='ceaopd',
            name='tests_ordered',
            field=models.ManyToManyField(blank=True, related_name='tests_ordered', to='bcpp_subject.TestsOrdered', verbose_name='If yes, indicate which of the following were ordered.'),
        ),
    ]
