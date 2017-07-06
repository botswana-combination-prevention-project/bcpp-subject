from datetime import date, timedelta
from django.test import TestCase
from edc_constants.choices import NO, YES
from model_mommy import mommy

from ..forms import PregnancyForm
from .test_mixins import SubjectMixin


class TestPregnancyForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        mommy.make_recipe('bcpp_subject.reproductivehealth',
                          subject_visit=self.subject_visit_female, report_datetime=self.get_utcnow
                          (), currently_pregnant=YES)
        self.options = {
            'subject_visit': self.subject_visit_female.id,
            'report_datetime': self.get_utcnow(),
            'current_pregnant': NO,
            'anc_reg': YES,
            'lnmp': date.today()
        }

    def test_form_is_valid(self):
        form = PregnancyForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save)

    def test_none_lnmp_when_pregnant(self):
        self.options.update(current_pregnant=YES, lnmp=None)
        form = PregnancyForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_provide_lnmp_when_pregnant(self):
        demo_preg_lmnp_date = date.today() - timedelta(90)
        self.options.update(current_pregnant=YES, lnmp=demo_preg_lmnp_date)
        form = PregnancyForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_anc_registration_when_pregnant(self):
        self.options.update(current_pregnant=YES, anc_reg=None)
        form = PregnancyForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(current_pregnant=YES, anc_reg=YES)
        form = PregnancyForm(data=self.options)
        self.assertTrue(form.is_valid())
