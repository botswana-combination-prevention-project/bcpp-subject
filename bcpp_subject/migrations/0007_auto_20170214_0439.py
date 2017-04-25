# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-14 02:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0006_auto_20170213_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhivcareadherence',
            name='arv_evidence',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], help_text='Examples of evidence might be OPD card, tablets, masa number, etc.', max_length=3, verbose_name='<span style="color:orange;">Interviewer: </span> Is there evidence that the participant is on therapy?'),
        ),
        migrations.AlterField(
            model_name='historicalhivcareadherence',
            name='ever_recommended_arv',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer")], help_text='Common medicines include: combivir, truvada, atripla, nevirapine, dolutegravir', max_length=25, verbose_name='Have you ever been recommended by a doctor/nurse or other healthcare worker to start antiretroviral therapy (ARVs), a combination of medicines to treat your HIV infection? '),
        ),
        migrations.AlterField(
            model_name='historicalhivcareadherence',
            name='on_arv',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], help_text='If yes, need to answer next two questions.', max_length=25, verbose_name='Are you currently taking antiretroviral therapy (ARVs)?'),
        ),
        migrations.AlterField(
            model_name='historicalhivmedicalcare',
            name='lowest_cd4',
            field=models.CharField(choices=[('0-49', '0-49'), ('50-99', '50-99'), ('100-199', '100-199'), ('200-349', '200-349'), ('350-499', '350-499'), ('500 or more', '500 or more'), ('not_sure', 'I am not sure'), ('DWTA', "Don't want to answer")], help_text='Assist the participant by helping review their outpatient cards if they are available.', max_length=25, null=True, verbose_name='What was your lowest CD4 (masole) count that was ever measured?'),
        ),
        migrations.AlterField(
            model_name='historicalhivtested',
            name='why_hiv_test',
            field=models.CharField(choices=[('I was worried I might have HIV and wanted to know my status', 'I was worried I might have HIV and wanted to know my status'), ('I heard from someone I trust that it is important for me to get tested for HIV ', 'I heard from someone I trust that it is important for me to get tested for HIV '), ('I was at a health facility where the doctor/nurse recommended I get tested for HIV during the same visit', 'I was at a health facility where the doctor/nurse recommended I get tested for HIV during the same visit'), ('I read information on a brochure/flier that it is important for me to get tested for HIV', 'I read information on a brochure/flier that it is important for me to get tested for HIV'), ('from_ya_tsie', 'I had information from the Ya Tsie study that it was important to get tested for HIV'), ('OTHER', 'Other'), ('not_sure', 'I am not sure'), ('DWTA', "Don't want to answer")], max_length=105, null=True, verbose_name="Not including today's HIV test, which of the following statements best describes the reason you were tested the last most recent time you were tested before today?"),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='alcohol_sex',
            field=models.CharField(blank=True, choices=[('Neither of us', 'Neither of us'), ('My partner', 'My partner'), ('Myself', 'Myself'), ('Both of us', 'Both of us'), ('DWTA', "Don't want to answer")], max_length=25, null=True, verbose_name='During the last most recent time you had sex, were you or your partner drinking alcohol?'),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='condom',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer")], max_length=25, null=True, verbose_name='During the last most recent time you had sex, did you or your partner use a condom?'),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='ever_sex',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer")], max_length=25, verbose_name='In your lifetime, have you ever had sex with anyone? <span style="font-weight:normal;">(including your spouse, friends, or someone you have just met.)</span>'),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='first_sex',
            field=models.IntegerField(blank=True, help_text='Note:leave blank if participant does not want to respond.', null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(64)], verbose_name="How old were you when you had sex for the first time? If you can't recall the exact age, please give a best guess."),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='last_year_partners',
            field=models.IntegerField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></br>Leave blank if participant does not want to respond.</p>", null=True, verbose_name='In the past 12 months, how many different people have you had sex with?'),
        ),
        migrations.AlterField(
            model_name='historicalsexualbehaviour',
            name='lifetime_sex_partners',
            field=models.IntegerField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></p>", null=True, verbose_name='In your lifetime, how many different people have you had sex with?'),
        ),
        migrations.AlterField(
            model_name='hivcareadherence',
            name='arv_evidence',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], help_text='Examples of evidence might be OPD card, tablets, masa number, etc.', max_length=3, verbose_name='<span style="color:orange;">Interviewer: </span> Is there evidence that the participant is on therapy?'),
        ),
        migrations.AlterField(
            model_name='hivcareadherence',
            name='ever_recommended_arv',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer")], help_text='Common medicines include: combivir, truvada, atripla, nevirapine, dolutegravir', max_length=25, verbose_name='Have you ever been recommended by a doctor/nurse or other healthcare worker to start antiretroviral therapy (ARVs), a combination of medicines to treat your HIV infection? '),
        ),
        migrations.AlterField(
            model_name='hivcareadherence',
            name='on_arv',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], help_text='If yes, need to answer next two questions.', max_length=25, verbose_name='Are you currently taking antiretroviral therapy (ARVs)?'),
        ),
        migrations.AlterField(
            model_name='hivmedicalcare',
            name='lowest_cd4',
            field=models.CharField(choices=[('0-49', '0-49'), ('50-99', '50-99'), ('100-199', '100-199'), ('200-349', '200-349'), ('350-499', '350-499'), ('500 or more', '500 or more'), ('not_sure', 'I am not sure'), ('DWTA', "Don't want to answer")], help_text='Assist the participant by helping review their outpatient cards if they are available.', max_length=25, null=True, verbose_name='What was your lowest CD4 (masole) count that was ever measured?'),
        ),
        migrations.AlterField(
            model_name='hivtested',
            name='why_hiv_test',
            field=models.CharField(choices=[('I was worried I might have HIV and wanted to know my status', 'I was worried I might have HIV and wanted to know my status'), ('I heard from someone I trust that it is important for me to get tested for HIV ', 'I heard from someone I trust that it is important for me to get tested for HIV '), ('I was at a health facility where the doctor/nurse recommended I get tested for HIV during the same visit', 'I was at a health facility where the doctor/nurse recommended I get tested for HIV during the same visit'), ('I read information on a brochure/flier that it is important for me to get tested for HIV', 'I read information on a brochure/flier that it is important for me to get tested for HIV'), ('from_ya_tsie', 'I had information from the Ya Tsie study that it was important to get tested for HIV'), ('OTHER', 'Other'), ('not_sure', 'I am not sure'), ('DWTA', "Don't want to answer")], max_length=105, null=True, verbose_name="Not including today's HIV test, which of the following statements best describes the reason you were tested the last most recent time you were tested before today?"),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='alcohol_sex',
            field=models.CharField(blank=True, choices=[('Neither of us', 'Neither of us'), ('My partner', 'My partner'), ('Myself', 'Myself'), ('Both of us', 'Both of us'), ('DWTA', "Don't want to answer")], max_length=25, null=True, verbose_name='During the last most recent time you had sex, were you or your partner drinking alcohol?'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='condom',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer")], max_length=25, null=True, verbose_name='During the last most recent time you had sex, did you or your partner use a condom?'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='ever_sex',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('DWTA', "Don't want to answer")], max_length=25, verbose_name='In your lifetime, have you ever had sex with anyone? <span style="font-weight:normal;">(including your spouse, friends, or someone you have just met.)</span>'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='first_sex',
            field=models.IntegerField(blank=True, help_text='Note:leave blank if participant does not want to respond.', null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(64)], verbose_name="How old were you when you had sex for the first time? If you can't recall the exact age, please give a best guess."),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='last_year_partners',
            field=models.IntegerField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></br>Leave blank if participant does not want to respond.</p>", null=True, verbose_name='In the past 12 months, how many different people have you had sex with?'),
        ),
        migrations.AlterField(
            model_name='sexualbehaviour',
            name='lifetime_sex_partners',
            field=models.IntegerField(blank=True, help_text="<p><i>Please remember to include casual and once-off partners</br>(prostitutes and truck drivers) as well as long-term partners</br>(spouses, boyfriends/girlfriends).<br>If you can't recall the exact number, please give a best guess.</i></p>", null=True, verbose_name='In your lifetime, how many different people have you had sex with?'),
        ),
    ]