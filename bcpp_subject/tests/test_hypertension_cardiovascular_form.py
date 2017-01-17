from django.test import TestCase

from edc_constants.constants import NO, NOT_APPLICABLE, YES, NEVER 
from model_mommy import mommy

from ..forms import HypertensionCardiovascularForm

from .test_mixins import SubjectMixin


class TestHypertensionCardiovascular(SubjectMixin, TestCase):

    def setUp(self):
        """Initial data set to valid"""
        super().setUp()

        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }

        self.medication_taken = mommy.make_recipe('bcpp_subject.medication_taken')

        self.medication_given = mommy.make_recipe('bcpp_subject.medication_given')

        self.medication_taken_1 = mommy.make_recipe('bcpp_subject.medication_taken_1')

        subject_visit = self.make_subject_visit_for_consented_subject_male(
            'T0', **self.consent_data)

        self.data = {
            'may_take_blood_pressure': NO,
            'hypertension_diagnosis': NOT_APPLICABLE,
            'medications_taken': [self.medication_taken.id, self.medication_taken_1.id],
            'if_other_medications_taken': 'some_medication',
            'medication_still_given': [self.medication_given.id],
            'if_other_medication_still_given': None,
            'health_care_facility': NOT_APPLICABLE,
            'salt_intake_counselling': NOT_APPLICABLE,
            'tobacco_smoking': NOT_APPLICABLE,
            'tobacco_counselling': NOT_APPLICABLE,
            'weight_counselling': NOT_APPLICABLE,
            'physical_activity_counselling': NOT_APPLICABLE,
            'alcohol_counselling': NOT_APPLICABLE,
            'blood_test_for_cholesterol': NOT_APPLICABLE,
            'blood_test_for_diabetes': NOT_APPLICABLE,
            'subject_visit': subject_visit.id,
            'report_datetime': self.get_utcnow()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_validate_if_other_medication_taken(self):
        """Test to verify whether validation will fire when
        'other' is selected in medications_taken but
        if_other_medications_taken is left empty"""
        self.data.update(if_other_medications_taken=None)
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_validate_if_other_medication_taken_false(self):
        """Test to verify whether validation will fire when
        'other' is not selected in medications_taken but
        if_other_medications_taken is filled"""
        self.data.update(
            medications_taken=[self.medication_taken.id],
            if_other_medications_taken='some_medication')
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())
