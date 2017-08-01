from django.test import TestCase, tag

from edc_constants.constants import YES, NO

from ..forms import PimaCd4Form
from .test_mixins import SubjectMixin


@tag('PIMA')
class TestPimaCd4Form(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.options = {
            'pima_today': YES,
            'pima_today_other': 'Failed Blood Collection',
            'pima_id': 12345,
            'cd4_datetime': self.get_utcnow(),
            'cd4_value': 400.00,
            'subject_visit': self.subject_visit_female.id,
            'report_datetime': self.get_utcnow()
        }
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save)

    def test_pima_today(self):
        """Assert if pima_day eq YES, then no need to
        provide other reasons.
        """
        self.options.update(pima_today=YES, pima_today_other=None)
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())
        self.options.update(
            pima_today=NO,
            pima_today_other=None)
        form = PimaCd4Form(data=self.options)
        self.assertFalse(form.is_valid())
        self.options.update(
            pima_today=NO,
            pima_today_other="Failed Blood Collection",
            pima_id=None,
            cd4_value=None)
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())

    def test_pima_id_not_required(self):
        """ Assert if pima_today eq NO then pimaa_id not required.
        """
        self.options.update(
            pima_today=NO,
            pima_id=None,
            cd4_value=None)
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())
        self.options.update(
            pima_today=NO,
            pima_id="100232")
        form = PimaCd4Form(data=self.options)
        self.assertFalse(form.is_valid())

    def test_pima_id_required(self):
        """Assert if pima_today eq YES then pima id is required.
        """
        self.options.update(pima_today=YES, pima_id="100232")
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())

        self.options.update(pima_today=YES, pima_id=None)
        form = PimaCd4Form(data=self.options)
        self.assertFalse(form.is_valid())

    def test_cd4_required(self):
        """Assert if pima_today eq YES then pima cd4 is required.
        """
        self.options.update(
            pima_today=YES,
            cd4_value=400.0)
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())
        self.options.update(pima_today=YES, cd4_value=None)
        form = PimaCd4Form(data=self.options)
        self.assertFalse(form.is_valid())

    def test_cd4_datetime_required(self):
        """Assert if pima_today eq YES then pima cd4_datetime
        is required.
        """
        self.options.update(
            pima_today=YES,
            cd4_datetime=self.get_utcnow())
        form = PimaCd4Form(data=self.options)
        self.assertTrue(form.is_valid())
        self.options.update(
            pima_today=YES,
            cd4_datetime=None)
        form = PimaCd4Form(data=self.options)
        self.assertFalse(form.is_valid())
