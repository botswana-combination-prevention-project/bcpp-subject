import datetime

from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import NO, YES, POS, NEG
from edc_metadata.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from .test_mixins import SubjectMixin
from edc_appointment.models import Appointment

from bcpp_subject.constants import T0, T1, T2
from datetime import timedelta


class TestAnnualRuleSurveyRuleGroups(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.visit_code = 'T1'
        self.bhs_subject_visit = self.make_subject_visit_for_a_male_subject(T0)
        self.subject_identifier = self.bhs_subject_visit.subject_identifier
        self.ahs_subject_visit_male_y2 = None
        self.ahs_subject_visit_male_y3 = None

    def crf_metadata_obj(self, model, entry_status, visit_code):
        return CrfMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            visit_code=visit_code,
            subject_identifier=self.subject_identifier)

    def requisition_metadata_obj(self, model, entry_status, visit_code, panel_name):
        return RequisitionMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            subject_identifier=self.subject_identifier,
            panel_name=panel_name,
            visit_code=visit_code)

    def hiv_result(self, status, subject_visit):
        """ Create HivResult for a particular survey"""
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Microtube',
        )
        hiv_result = mommy.make_recipe(
            'bcpp_subject.hivresult', subject_visit=subject_visit, report_datetime=self.get_utcnow(),
            hiv_result=status, insufficient_vol=NO
        )
        return hiv_result

    def test_no_circumsition_in_y2(self):
        """Assert that circumcision forms are not required at ahs if filled at bhs."""
#         self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcision', REQUIRED, 'T0').count(), 1)
#         self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcised', NOT_REQUIRED, 'T0').count(), 1)
#         self.assertEqual(self.crf_metadata_obj('bcpp_subject.uncircumcised', NOT_REQUIRED, 'T0').count(), 1)
        mommy.make_recipe(
            'bcpp_subject.circumcision',
            subject_visit=self.bhs_subject_visit,
            circumcised=YES,
            report_datetime=self.get_utcnow()
        )
        mommy.make_recipe(
            'bcpp_subject.circumcised',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow(),
            where_circ='Lobatse',
            why_circ='not_sure'
        )
        bhs_household_member = self.bhs_subject_visit.household_member
        # Create an ahs member
        household_member = super().make_ahs_household_member(bhs_household_member)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=self.visit_code)

        mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcision', NOT_REQUIRED, self.visit_code).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcised', NOT_REQUIRED, self.visit_code).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.uncircumcised', NOT_REQUIRED, self.visit_code).count(), 1)

    def test_pos_in_y1_no_hiv_forms(self):

        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        self._hiv_result = self.hiv_result(POS, self.bhs_subject_visit)

        household_member = super().make_ahs_household_member(self.bhs_subject_visit.household_member)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=self.visit_code)

        mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        microtube_options = {}
        microtube_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Microtube',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtested', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresultdocumentation', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestinghistory', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, 'Microtube').count(), 1)

    def test_hic_filled_in_y1_notrequired_in_annual(self):
        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        self.hiv_result(NEG, self.bhs_subject_visit)

        mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            hic_permission=YES)

        subject_visit_male = self.annual_subject_visit_y2

        self.hiv_result(NEG, subject_visit_male)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T1).count(), 1)

        subject_visit_male_T2 = self.annual_subject_visit_y3

        self.hiv_result(NEG, subject_visit_male_T2)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T2).count(), 1)

    def test_microtube_always_required_for_hic_without_pos_hivresult(self):
        """ Tests that an HIC enrollee who sero-converted to POS status, but the POS result not tested by BHP,
            will be tested by BHP at next visit. """
        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        self.hiv_result(NEG, self.bhs_subject_visit)

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            permanent_resident=YES,
            intend_residency=NO)

        mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            hic_permission=YES)

        self.ahs_subject_visit_male = None  # TODO: created ahs year 2 visit, self.annual_subject_visit_y2

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T2).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, 'Microtube').count(), 1)
        # Make participant known positive in year 2, microtube and hiv result should remain required
        # NOTE: We are using HivTestingHistory and HivTestReview to create the POS status because the participant
        # was not tested by BHP, they became POS after our last visit with them.
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.ahs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )
        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.ahs_subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, 'Microtube').count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T2).count(), 1)

    def test_microtube_not_required_for_hic_with_pos_hivresult(self):
        """ Tests that an HIC enrollee who sero-converted to POS status, tested by BHP, will not be tested
            again in next visit."""
        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        self.hiv_result(NEG, self.bhs_subject_visit)

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            permanent_resident=YES,
            intend_residency=NO)

        mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            hic_permission=YES)

        self.subject_visit_male_y2 = None  # TODO: create year 2 subject_visit self.annual_subject_visit_y2
        # Make participant known positive in year 2, tested by BHP. That means hey have an HivResult record with POS
        # NOTE: We are using HivResult to indicate that the HIV POS result was tested by BHP.
        self.hiv_result(POS, self.subject_visit_male_y2)
        # We are now in year 3 in which the participant is a known POS.
        self.subject_visit_male_y3 = None  # TODO, create year 3 subjectvisit

        microtube_options = {}
        microtube_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Microtube',
            appointment=self.subject_visit_male_T2.appointment)
        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, 'Microtube').count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T2).count(), 1)

    def test_hiv_pos_requisitions_y2(self):
        """ HIV Negative and in HIC at T0 and Tests Positive during home visits at T1 and is Not on ART at T1.
            Sero Converter, Should offer POC CD4, RBD and VL.
        """

        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            permanent_resident=YES,
            intend_residency=NO)

        self.hiv_result(NEG, self.bhs_subject_visit)

        mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            hic_permission=YES)

        self.subject_visit_male_y3 = None # TODO create t2 subject visit, self.annual_subject_visit_y2

        self.hiv_result(POS, self.subject_visit_male_y3)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, 'VIRAL LOAD').count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, 'Research Blood Draw').count(), 1)

    def test_Known_hiv_pos_y2_not_hic_require_no_testing(self):

        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        # They were NEG in year 1
        self.hiv_result(POS, self.bhs_subject_visit_male)

        self.subject_visit_male = None  #self.annual_subject_visit_y2

        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T1).count(), 1)

        self.ahs_subject_visit_male_y3 = None  # self.annual_subject_visit_y3

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T2).count(), 1)

    def test_Known_hiv_pos_y3_not_hic_require_no_testing_missed_y2(self):
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier
        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.bhs_subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)

        # Misses T1, and is seen again at T2. They should not be Tested.
        self.ahs_subject_visit_male_y3 = None  # self.annual_subject_visit_y3

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T2).count(), 1)

    def test_hic_enrolled_at_bhs(self):
        """ If there is an hic record at bhs then at ahs inspect the record then check for hic status if not enrolled then Hic_enrollment
            should be filled otherwise should not be filled.
        """
        self.subject_identifier = self.bhs_subject_visit.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=self.bhs_subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            permanent_resident=YES,
            intend_residency=NO)

        self.hiv_result(NEG, self.bhs_subject_visit_male)

        mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            hic_permission=YES)

        self.ahs_subject_visit_male_y2 = None  # self.ahs_subject_visit_male_y2

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T1).count(), 1)

        self.ahs_subject_visit_male_y3 = None  # self.annual_subject_visit_y3

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T2).count(), 1)

    def test_hic_not_enrolled_at_bhs(self):
        """ If there is an hic record inspect the record then check for hic status if not enrolled then Hic_enrollment
            should be offered again at T1.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            permanent_resident=YES,
            intend_residency=NO)

        self.hiv_result(NEG, self.bhs_subject_visit_male)

        mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            hic_permission=NO)

        self.ahs_subject_visit_male_y2 = None  # self.annual_subject_visit_y2

        self.hiv_result(NEG, self.ahs_subject_visit_male_y2)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', REQUIRED, T1).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs_new_erollee(self):
        """New enrollees at T0 (i.e doing BHS procedures) who are HIV-positive and ART naive, then PIMA required.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        self.ahs_subject_visit_male_y2 = None  # self.annual_subject_visit_y2

        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.bhs_subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)

    def hiv_pos_nd_art_naive_at_bhs(self):
        """Enrollees at t0 who are HIV-positive and ART naive at BHS.
           Pima, RBD and VL required. Then Key RBD for later use in Annual survey.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.bhs_subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, 'Research Blood Draw').count(), 1)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Research Blood Draw',
        )
        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T0).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T0, 'VIRAL LOAD').count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', KEYED, T0, 'Research Blood Draw').count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART, (i.e arv_naive) at the time of enrollment.
           Still arv_naive at AHS. Pima and VL required. RBD keyed in T0, so not required.
        """
        self.hiv_pos_nd_art_naive_at_bhs()

        self.ahs_subject_visit_male_y2 = self.annual_subject_visit_y2
        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.ahs_subject_visit_male_y2,
            report_datetime=self.get_utcnow(),
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, 'VIRAL LOAD').count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, 'Research Blood Draw').count(), 1)

    def test_hiv_pos_nd_on_art_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e arv_naive) at the time of enrollment.
           But now on ART at T1. Pima and VL required at T1(rule: art naive at enrollment).
           RBD keyed in T0, so not required. POC VL not required at T1.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.bhs_subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T0, 'Research Blood Draw').count(), 1)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Research Blood Draw',
        )
        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name='Research Blood Draw',
        )

        self.ahs_subject_visit_male_y2 = None # self.annual_subject_visit_y2

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.ahs_subject_visit_male_y2,
            report_datetime=self.get_utcnow(),
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, 'VIRAL LOAD').count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, 'Research Blood Draw').count(), 1)

        self.ahs_subject_visit_male_y3 = None

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.ahs_subject_visit_male_y3,
            report_datetime=self.get_utcnow(),
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, 'VIRAL LOAD').count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, 'Research Blood Draw').count(), 1)

#     def test_hiv_pos_nd_on_art_at_y3_missed_y2(self):
#         """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e arv_naive) at the time of enrollment.
#            Misses T1. But now on ART at T2. Pima and VL required at T2(rule: art naive at enrollment).
#            RBD keyed in T0, so not required. POC VL not required at T2.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         #         self.hiv_result(POS, self.subject_visit_male_T0)
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
# 
#         # self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pimavl_options).count(), 1)
# 
#         aliquot_type = AliquotType.objects.all()[0]
#         site = self.study_site
#         rbd = Panel.objects.get(name='Research Blood Draw')
#         SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)
# 
#         self.subject_visit_male_T2 = self.annual_subject_visit_y3
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T2.appointment)
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male_T2.appointment)
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T2.appointment)
#         pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)
# 
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T2,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=YES,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def test_hiv_pos_nd_not_on_art_at_bhs(self):
#         """HIV Positive not on ART at T0, Should offer POC CD4, RBD and VL.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         hiv_car_adherence_options = {}
#         hiv_car_adherence_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivcareadherence',
#             appointment=self.subject_visit_male_T0.appointment)
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
# 
#     def test_hiv_pos_nd_not_on_art_at_ahs(self):
#         """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e art_naive) at the time of enrollment. Pima required.
#            Still HIV Positive and still not on ART at T1: Should offer POC CD4 and VL. No RBD
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         hiv_car_adherence_options = {}
#         hiv_car_adherence_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivcareadherence',
#             appointment=self.subject_visit_male_T0.appointment)
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T0.appointment)
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male_T0.appointment)
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male_T0.appointment)
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **hiv_car_adherence_options).count(), 1)
#         # ART naive at the time of enrollment, in this case T0.
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
# 
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
# 
#         aliquot_type = AliquotType.objects.all()[0]
#         site = self.study_site
#         rbd = Panel.objects.get(name='Research Blood Draw')
#         SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)
# 
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED, **research_blood_draw_options).count(), 1)
# 
#         # Move on to the first annual visit.
#         self.subject_visit_male = self.annual_subject_visit_y2
#         hiv_car_adherence_options.update(appointment=self.subject_visit_male.appointment)
#         pimavl_options.update(appointment=self.subject_visit_male.appointment)
#         pima_options.update(appointment=self.subject_visit_male.appointment)
#         research_blood_draw_options.update(appointment=self.subject_visit_male.appointment)
#         viral_load_options.update(appointment=self.subject_visit_male.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
# 
#         # Move on to the second annual visit.
#         self.subject_visit_male_T2 = self.annual_subject_visit_y3
#         hiv_car_adherence_options.update(appointment=self.subject_visit_male_T2.appointment)
#         pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)
#         pima_options.update(appointment=self.subject_visit_male_T2.appointment)
#         research_blood_draw_options.update(appointment=self.subject_visit_male_T2.appointment)
#         viral_load_options.update(appointment=self.subject_visit_male_T2.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def test_hiv_pos_nd_not_on_art_at_y3_missed_y2(self):
#         """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e art_naive) at the time of enrollment. Pima required.
#            Misses T1. Found at T2 still HIV Positive and still not on ART: Should offer POC CD4 and VL. No RBD.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         hiv_car_adherence_options = {}
#         hiv_car_adherence_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivcareadherence',
#             appointment=self.subject_visit_male_T0.appointment)
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T0.appointment)
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male_T0.appointment)
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male_T0.appointment)
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **hiv_car_adherence_options).count(), 1)
#         # ART naive at the time of enrollment, in this case T0.
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
# 
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
# 
#         aliquot_type = AliquotType.objects.all()[0]
#         site = self.study_site
#         rbd = Panel.objects.get(name='Research Blood Draw')
#         SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)
# 
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED, **research_blood_draw_options).count(), 1)
# 
#         # JUMP first annual visit. Move on to the second annual visit.
#         self.subject_visit_male_T2 = self.annual_subject_visit_y3
#         hiv_car_adherence_options.update(appointment=self.subject_visit_male_T2.appointment)
#         pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)
#         pima_options.update(appointment=self.subject_visit_male_T2.appointment)
#         research_blood_draw_options.update(appointment=self.subject_visit_male_T2.appointment)
#         viral_load_options.update(appointment=self.subject_visit_male_T2.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def test_hiv_pos_nd_on_art_at_ahs1(self):
#         """Previously enrollees at t0 who are HIV-positive but were not on ART naive at the time of enrollment. Pima required.
#            HIV Positive not on ART at T1: Should offer POC CD4 and VL.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=YES,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
# 
#         self.subject_visit_male_T2 = self.annual_subject_visit_y3
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T2,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=YES,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
# 
#     def test_hiv_pos_nd_not_art_at_y1_misses_y2(self):
#         """Previously enrollees at t0 who are HIV-positive but were ART naive at the time of enrollment. Pima required.
#            Misses T2. HIV Positive and on ART at T3: Should offer POC CD4 and VL.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
# 
#         self.subject_visit_male_T2 = self.annual_subject_visit_y3
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T2,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=YES,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
# 
#     def hiv_pos_nd_on_art_bhs(self):
#         """Enrollees at t0 who are HIV-positive and on ART at the time of enrollment.
#            Pima and POC VL NOT required. RBD, VL required.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         self.hiv_result(POS, self.subject_visit_male_T0)
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=YES,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
#         #self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pimavl_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def hiv_pos_nd_on_art_ahs(self):
#         """Previously enrollees at t0 who are HIV-positive on ART at the time of enrollment.
#            Pima and POC VL NOT required. RBD, VL required.
#         """
#         self.hiv_pos_nd_on_art_bhs()
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male.appointment)
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)
# 
#         self.subject_visit_male = self.annual_subject_visit_y3
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male_T2.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
#         #self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pimavl_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)
# 
#     def test_hiv_neg_bhs_and_pos_at_ahs(self):
#         """ HIV Negative and in HIC at T0 and now HIV POS not on ART at T1, should Offer POC CD4, RBD and VL and PIMA VL.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)
# 
#         self.hiv_result(NEG, self.subject_visit_male_T0)
# 
#         SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
#                               subject_visit=self.subject_visit_male_T0)
# 
#         HicEnrollment.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             report_datetime=datetime.today(),
#             hic_permission=YES)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male.appointment)
# 
#         viral_load_options = {}
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         pimavl_options = {}
#         pimavl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.hiv_result(POS, self.subject_visit_male)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def hiv_pos_at_bhs_and_hiv_care_adherence_is_required(self):
#         """Enrollees at t0 who are HIV-positive and on ART at the time of enrollment.
#            Pima and POC VL NOT required. RBD, VL required.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         self.hiv_result(POS, self.subject_visit_male_T0)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         hiv_care_adherence_options = {}
#         hiv_care_adherence_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivcareadherence',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(
#             entry_status=REQUIRED, **hiv_care_adherence_options).count(), 1)
# 
#     def test_not_known_pos_runs_hiv_and_cd4_ahs(self):
#         """If not a known POS, requires HIV and CD4 (until today's result is known)."""
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
#                               subject_visit=self.subject_visit_male_T0)
# 
#         self.hiv_result('Declined', self.subject_visit_male_T0)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         viral_load_options = {}
#         hiv_result_options = {}
#         research_blood_draw_options = {}
# 
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male.appointment)
# 
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
#         hiv_result_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivresult',
#             appointment=self.subject_visit_male.appointment)
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.hiv_result(POS, self.subject_visit_male)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def test_not_known_neg_runs_hiv_and_cd4_ahs_1(self):
#         """If not a known POS, requires HIV and CD4 (until today's result is known)."""
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
#                               subject_visit=self.subject_visit_male_T0)
# 
#         self.hiv_result(NEG, self.subject_visit_male_T0)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         viral_load_options = {}
#         hiv_result_options = {}
# 
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
#         hiv_result_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivresult',
#             appointment=self.subject_visit_male.appointment)
# 
#         research_blood_draw_options = {}
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male.appointment)
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.hiv_result("Declined", self.subject_visit_male)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)
# 
#     def test_not_known_pos_runs_hiv_and_cd4_ahs_2(self):
#         """If not a known POS, requires HIV and CD4 (until today's result is known)."""
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
#                               subject_visit=self.subject_visit_male_T0)
# 
#         self.hiv_result(POS, self.subject_visit_male_T0)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         viral_load_options = {}
#         hiv_result_options = {}
# 
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
#         hiv_result_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivresult',
#             appointment=self.subject_visit_male.appointment)
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.hiv_result("Declined", self.subject_visit_male)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
# 
# 
#     def test_not_known_pos_runs_hiv_and_cd4_ahs_y3(self):
#         """If not a known POS, requires HIV and CD4 (until today's result is known)."""
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
#                               subject_visit=self.subject_visit_male_T0)
# 
#         self.hiv_result('Declined', self.subject_visit_male_T0)
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested="DWTA",
#             when_hiv_test='1 to 5 months ago',
#             has_record="Don't want to answer",
#             verbal_hiv_result='not_answering',
#             other_record=NO
#         )
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         self.hiv_result('Declined', self.subject_visit_male)
# 
# 
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male,
#             has_tested="DWTA",
#             when_hiv_test='1 to 5 months ago',
#             has_record="Don't want to answer",
#             verbal_hiv_result='not_answering',
#             other_record=NO
#         )
# 
#         subject_visit_male_T2 = self.annual_subject_visit_y3
# 
#         viral_load_options = {}
#         hiv_result_options = {}
# 
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=subject_visit_male_T2.appointment)
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=subject_visit_male_T2.appointment)
# 
#         HivTestingHistory.objects.create(
#             subject_visit=subject_visit_male_T2,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
# 
#         self.hiv_result(POS, subject_visit_male_T2)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
# 
#     def test_not_known_neg_runs_hiv_and_cd4_ahs(self):
#         """If not a known POS, requires HIV and CD4 (until today's result is known)."""
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
#                               subject_visit=self.subject_visit_male_T0)
# 
#         self.hiv_result('Declined', self.subject_visit_male_T0)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         viral_load_options = {}
#         hiv_result_options = {}
#         research_blood_draw_options = {}
# 
#         research_blood_draw_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             appointment=self.subject_visit_male.appointment)
# 
#         viral_load_options.update(
#             lab_entry__app_label='bcpp_lab',
#             lab_entry__model_name='subjectrequisition',
#             lab_entry__requisition_panel__name='Viral Load',
#             appointment=self.subject_visit_male.appointment)
#         hiv_result_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivresult',
#             appointment=self.subject_visit_male.appointment)
# 
#         pima_options = {}
#         pima_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pima',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.hiv_result(NEG, self.subject_visit_male)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)
#         self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
# 
#     def test_hiv_pos_nd_art_naive_at_ahs_require_linkage_to_care(self):
#         """Previously enrollees at t0 who are HIV-positive but were not on ART, (i.e arv_naive) at the time of enrollment.
#            Still arv_naive at AHS. HIV linkage to care required.
#         """
#         self.hiv_pos_nd_art_naive_at_bhs()
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.hiv_result(POS, self.subject_visit_male)
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care=YES,
#             ever_recommended_arv=NO,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **linkage_to_care_options).count(), 1)
# 
#     def test_newly_pos_and_not_art_bhs_not_require_linkage_to_care(self):
#         """Newly HIV Positive not on ART at T0, Should not offer hiv linkage to care.
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
# 
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,
#         )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
# 
#     def test_pos_on_art_notrequire_linkage_to_care(self):
#         """If POS and on arv and have doc evidence, Hiv Linkage to care not required, not a defaulter."""
# 
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
# 
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=YES,
#             arv_evidence=YES,
#         )
# 
#         # on art so no need for CD4
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
# 
#     def test_known_neg_does_not_require_linkage_to_care(self):
#         """If previous result is NEG, does not require hiv linkage to care.
# 
#         See rule_groups.ReviewNotPositiveRuleGroup
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male.appointment)
# 
#         self._hiv_result = self.hiv_result(NEG, self.subject_visit_male)
#         # add HivCarAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=YES,
#             arv_evidence=YES,
#         )
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
# 
#     def test_known_pos_defaulter_require_linkage_to_care(self):
#         """If previous result is POS on art but no evidence.
# 
#         This is a defaulter
# 
#         See rule_groups.ReviewNotPositiveRuleGroup
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         # add HivTestReview,
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         # add HivCareAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=YES,
#             on_arv=NO,
#             arv_evidence=YES,  # this is the rule field
#         )
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **linkage_to_care_options).count(), 1)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male.appointment)
# 
#         # add HivCareAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=YES,  # this is the rule field
#         )
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **linkage_to_care_options).count(), 1)
# 
#     def test_known_pos_not_require_linkage_to_care(self):
#         """If previous result is POS on art but no evidence.
# 
#         See rule_groups.ReviewNotPositiveRuleGroup
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         # add HivTestReview,
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
# 
#         # add HivCareAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=YES,
#             on_arv=YES,
#             arv_evidence=YES,  # this is the rule field
#         )
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male_T0.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
# 
#         self.subject_visit_male = self.annual_subject_visit_y2
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male.appointment)
# 
#         # add HivCareAdherence,
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=YES,  # this is the rule field
#         )
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
# 
#     def test_known_neg_does_requires_hiv_linkage_to_care(self):
#         """If previous result is NEG, does not need Hiv linkage to care.
# 
#         See rule_groups.ReviewNotPositiveRuleGroup
#         """
#         self.subject_visit_male_T0 = self.baseline_subject_visit
# 
#         self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)
#         self.subject_visit_male = self.annual_subject_visit_y2
# 
#         linkage_to_care_options = {}
#         linkage_to_care_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivlinkagetocare',
#             appointment=self.subject_visit_male.appointment)
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
