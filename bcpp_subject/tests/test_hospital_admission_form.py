from django.test import TestCase

from edc_constants.constants import YES

from .test_mixins import SubjectMixin

from ..forms import HospitalAdmissionForm

# from member.models.household_member import HouseholdMember
# from member.models.household_member.HouseholdMember import household_structure

from ..constants import T1

from dateutil.relativedelta import relativedelta


class TestHospitalAdmissionForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()

        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        self.add_enrollment_checklist(old_member)
#         self.add_subject_consent(old_member)

        self.consent_data = {
            'identity': '31722515',
            'confirm_identity': '31722515',
            'report_datetime': self.get_utcnow(),
        }

        report_datetime = self.get_utcnow() + relativedelta(years=1)
        self.t1_visit = self.add_subject_visit_followup(old_member, T1, report_datetime)

        self.subject_visit_t1 = self.make_subject_visit_for_consented_subject_male('T1', **self.consent_data)

        next_household_structure = self.get_next_household_structure_ready(
            old_member.household_structure, make_hoh=None)

        self.t1_visit = self.add_subject_visit_followup(old_member.next_household_structure, T1, report_datetime)

        self.options = {
           'subject_visit': self.subject_visit_t1.id,
           '÷≥lreport_ datetime': self.get_utcnow()+ relativedelta(years=1),
           'admission_nights': 2,
           'reason_hospitalized': 'Pregnancy',
           'facility_hospitalized': 'Clinic',
           'nights_hospitalized':  2,
           'healthcare_expense': 100.00,
           'travel_hours': '1 to under 2 hours',
           'total_expenses': 100.00,
           'hospitalization_costs': YES,
           'household_structure': self.household_structure.id,
           'old_member': self.old_member.id,
           'next_household_structure': self.next_household_structure.id,
           't1_visit': self.t1_visit.id,
        }

    def test_form_is_valid(self):
        form = HospitalAdmissionForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_zero_admission_nights_with_reason_hospitalized(self):
        """Asserts zero admission nights must have
        none hospitalization reason"""
        self.options.update(admission_nights=0)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_zero_admission_nights_with_travel_hours(self):
        """Asserts zero admission nights must have
        none travel hours"""
        self.options.update(admission_nights=0)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_zero_admission_nights_with_hospitalization_costs(self):
        """Asserts zero admission nights must have
        none hospitalization_costs"""
        self.options.update(admission_nights=0)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_reason_hospitalized(self):
        """Asserts zero admission nights must have
        none reason_hospitalized"""
        self.options.update(reason_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_travel_hours(self):
        """Asserts zero admission nights must have travel_hours"""
        self.options.update(travel_hours=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_facility_hospitalized(self):
        """Asserts admission nights must have facility_hospitalized"""
        self.options.update(facility_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_nights_hospitalized(self):
        """Asserts admission nights must have nights_hospitalized"""
        self.options.update(nights_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_healthcare_expense_gt_hospitalization_costs(self):
        """Asserts healthcare_expense must have hospitalization_costs"""
        self.options.update(hospitalization_costs=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_total_expenses_gt_hospitalization_costs(self):
        """Asserts total_expenses must have hospitalization_costs"""
        self.options.update(hospitalization_costs=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_save_form(self):
        form = HospitalAdmissionForm(data=self.options)
        self.assertTrue(form.save())
