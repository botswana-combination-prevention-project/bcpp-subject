# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-22 19:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0023_auto_20170219_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='first_sex_partner_age',
            field=models.CharField(choices=[('lte_18', 'less or equal to 18 years old'), ('gte_19', '19 years old or older'), ('dont_know', 'Not sure'), ('DWTA', "Don't want to answer"), ('N/A', 'Not applicable')], default='N/A', max_length=25, verbose_name='How old was your sex partner when you had sex for the first time'),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='last_year_partners',
            field=models.CharField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></br>Leave blank if participant does not want to respond.</p>", max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Expected a number greater than or equal to zero')], verbose_name='In the past 12 months, how many different people have you had sex with?'),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='lifetime_sex_partners',
            field=models.CharField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></p>", max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Expected a number greater than or equal to zero')], verbose_name='In your lifetime, how many different people have you had sex with?'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='first_sex_partner_age',
            field=models.CharField(choices=[('lte_18', 'less or equal to 18 years old'), ('gte_19', '19 years old or older'), ('dont_know', 'Not sure'), ('DWTA', "Don't want to answer"), ('N/A', 'Not applicable')], default='N/A', max_length=25, verbose_name='How old was your sex partner when you had sex for the first time'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='last_year_partners',
            field=models.CharField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></br>Leave blank if participant does not want to respond.</p>", max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Expected a number greater than or equal to zero')], verbose_name='In the past 12 months, how many different people have you had sex with?'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='lifetime_sex_partners',
            field=models.CharField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></p>", max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Expected a number greater than or equal to zero')], verbose_name='In your lifetime, how many different people have you had sex with?'),
        ),
    ]