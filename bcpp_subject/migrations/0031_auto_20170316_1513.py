# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django_crypto_fields.fields.encrypted_text_field
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0030_auto_20170316_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymousconsent',
            name='subject_identifier_as_pk',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalanonymousconsent',
            name='subject_identifier_as_pk',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalsubjectconsent',
            name='subject_identifier_as_pk',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='mail_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Mailing address '),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Physical address with detailed description'),
        ),
        migrations.AlterField(
            model_name='subjectconsent',
            name='subject_identifier_as_pk',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='mail_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Mailing address '),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Physical address with detailed description'),
        ),
    ]
