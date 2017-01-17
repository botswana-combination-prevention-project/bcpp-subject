from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc_constants.constants import YES, NO

from .test_mixins import SubjectMixin
from ..forms import HivCareAdherenceForm


class TestHivCareAdherence(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_female = self.make_subject_visit_for_consented_subject_female('T0', **self.consent_data)

        self.options = {
            'subject_visit': self.bhs_subject_visit_female.id,
            'first_positive': (self.get_utcnow() - relativedelta(years=1)).date(),
            'medical_care': YES,
            'no_medical_care': None,
            'ever_recommended_arv': YES,
            'ever_taken_arv': YES,
            'first_arv': (self.get_utcnow() - relativedelta(years=1)).date(),
            'on_arv': YES,
            'clinic_receiving_from': 'Bokaa',
            'next_appointment_date': (self.get_utcnow() - relativedelta(months=1)).date(),
            'arv_stop_date': None,
            'arv_stop': None,
            'adherence_4_day': 'Zero',
            'adherence_4_wk': 'Good',
            'arv_evidence': YES
        }

    def test_medical_care_no(self):
        """Assert form invalid when medical care is NO."""
        self.options.update(medical_care=NO)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_adherence_4_day_none(self):
        """Assert form invalid when on arv is yes and adherence for 4 days is none."""
        self.options.update(adherence_4_day=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_clinic_receiving_from_none(self):
        """Assert form invalid when on arv is yes and clinic receiving from is none."""
        self.options.update(clinic_receiving_from=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_next_appointment_date_none(self):
        """Assert form invalid when on arv is YES and next appointment date is none."""
        self.options.update(next_appointment_date=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_no_adherence_4_day_not_none(self):
        """Assert form invalid when on arv is NO and adherence for 4 days is not none."""
        self.options.update(on_arv=NO)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_arv_stop_date_not_null(self):
        """Assert form invalid when on arv is YES and arv stop date is not none."""
        self.options.update(on_arv=YES, arv_stop_date=date.today())
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_arv_stop_not_null(self):
        """Assert form invalid when on arv is YES and arv stop reason is not none."""
        self.options.update(on_arv=YES, arv_stop='Did not feel they were helping')
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_adherence_4_wk_null(self):
        """Assert form invalid when on arv is YES and adherence 4 weeks is none."""
        self.options.update(adherence_4_wk=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_taken_arv_yes_on_arv_no(self):
        """Assert form invalid when ever taken arv is YES and on arv is NO."""
        self.options.update(ever_taken_arv=YES, on_arv=NO)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_taken_arv_yes_arv_stop_date_null(self):
        """Assert form invalid when ever taken arv is YES and arv stop date is none."""
        self.options.update(ever_taken_arv=YES, arv_stop_date=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_taken_arv_yes_first_arv_null(self):
        """Assert form invalid when ever taken arv is YES and first arv date is none."""
        self.options.update(ever_taken_arv=YES, first_arv=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_taken_arv_no_arv_stop_not_null(self):
        """Assert form invalid when ever taken arv is NO and arv stop date is not none."""
        self.options.update(ever_taken_arv=NO)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_taken_arv_yes_why_no_arv_not_null(self):
        """Assert form invalid when ever taken arv is NO and reason why no arv is not none."""
        self.options.update(ever_taken_arv=YES, why_no_arv='Did not feel sick')
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_recommended_arv_yes_ever_taken_arv_no(self):
        """Assert form invalid when recommended arv is YES and ever taken arv is NO."""
        self.options.update(
            ever_recommended_arv=YES,
            ever_taken_arv=NO,
            why_no_arv=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_date_first_positive_today(self):
        """Assert form invalid when date first positive is today."""
        self.options.update(first_positive=date.today())
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_yes_arv_evidence_null(self):
        """Assert form invalid when on arv is YES and arv evidence is none"""
        self.options.update(on_arv=YES, arv_evidence=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_ever_taken_arv_no_on_arv_yes(self):
        """Assert form invalid when ever taken arv is YES and on arv is YES."""
        self.options.update(ever_taken_arv=YES, on_arv=YES)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_no_clinic_receiving_from_not_null(self):
        """Assert form invalid when on arv is NO and clinic receiving from is not none."""
        self.options.update(
            on_arv=NO,
            clinic_receiving_from='Bokaa',
            next_appointment_date=None)
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_on_arv_no_next_appointment_date_not_null(self):
        """Assert form invalid when on arv is NO and next appointment date from is not none."""
        self.options.update(
            on_arv=NO,
            clinic_receiving_from=None,
            next_appointment_date=(self.get_utcnow() - relativedelta(months=1)).date())
        form = HivCareAdherenceForm(data=self.options)
        self.assertFalse(form.is_valid())
