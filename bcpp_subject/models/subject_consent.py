from django.apps import apps as django_apps
from django.db import models

from edc_base.exceptions import AgeValueError
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_base.utils import age
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
    SampleCollectionFieldsMixin, CitizenFieldsMixin)
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_map.site_mappers import site_mappers
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin

from member.models import EnrollmentChecklist, HouseholdMember
from survey.model_mixins import SurveyModelMixin

from ..exceptions import ConsentValidationError
from ..managers import SubjectConsentManager

from .utils import get_enrollment_survey


def is_minor(dob, reference_datetime):
    return 16 <= age(dob, reference_datetime).years < 18


class SubjectConsent(
        ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin, NonUniqueSubjectIdentifierModelMixin,
        SurveyModelMixin, IdentityFieldsMixin, ReviewFieldsMixin,
        PersonalFieldsMixin, SampleCollectionFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin,
        BaseUuidModel):

    """ A model completed by the user that captures the ICF."""

    household_member = models.ForeignKey(HouseholdMember, on_delete=models.PROTECT)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(default=False, editable=False)

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier, self.version, ) + self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_subject.household_member']

    def __str__(self):
        return '{0} ({1}) V{2}'.format(self.subject_identifier, self.survey, self.version)

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey_schedule = self.household_member.survey_schedule_object.field_value
            self.survey = self.get_survey_name()
        self.study_site = site_mappers.current_map_code
        self.is_minor = YES if is_minor(self.dob, self.consent_datetime) else NO
        super().save(*args, **kwargs)

    def get_survey_name(self):
        return get_enrollment_survey(
            consents=SubjectConsent.objects.filter(
                identity=self.identity),
            survey_schedule_object=self.household_member.survey_schedule_object)

    def common_clean(self):
        # confirm member is eligible
        if not (self.household_member.age_in_years >= 16 and
                self.household_member.age_in_years <= 64 and
                self.household_member.study_resident == YES and
                self.household_member.inability_to_participate == NOT_APPLICABLE):
            raise ConsentValidationError('Member is not eligible for consent')
        # validate dob with HicEnrollment, if it exists
        HicEnrollment = django_apps.get_model(*'bcpp_subject.hicenrollment'.split('.'))
        try:
            HicEnrollment.objects.get(subject_visit__household_member=self.household_member)
            if self.dob != self.dob:
                raise ConsentValidationError('Does not match \'{}\'.'.format(
                    HicEnrollment._meta.verbose_name), 'dob')
        except HicEnrollment.DoesNotExist:
            pass
        # match with enrollment checklist.
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member__subject_identifier=self.household_member.subject_identifier, is_eligible=True)
        except EnrollmentChecklist.DoesNotExist:
            raise ConsentValidationError(
                'Member has not completed the \'{}\'. Please correct before continuing'.format(
                    EnrollmentChecklist._meta.verbose_name))
        # other model/form validations
        # match initials
        if not self.household_member.personal_details_changed == YES:
            if enrollment_checklist.initials != self.initials:
                raise ConsentValidationError('Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'initials')
        if self.dob:
            # minor (do this before comparing DoB)
            if (is_minor(enrollment_checklist.dob, enrollment_checklist.report_datetime) and not
                    is_minor(self.dob, self.consent_datetime)):
                if is_minor(enrollment_checklist.dob, enrollment_checklist.report_datetime):
                    raise ConsentValidationError(
                        'Subject is a minor by the {}.'.format(
                            EnrollmentChecklist._meta.verbose_name), 'dob')
                else:
                    raise ConsentValidationError(
                        'Subject is a not minor by the {}.'.format(
                            EnrollmentChecklist._meta.verbose_name), 'dob')
            # match DoB
            if enrollment_checklist.dob != self.dob:
                raise ConsentValidationError('Does not match \'{}\'. Expected {}.'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    enrollment_checklist.dob.strftime('%Y-%m-%d')), 'dob')
        # match gender
        if enrollment_checklist.gender != self.gender:
            raise ConsentValidationError(
                'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'gender')
        # minor and guardian name
        if enrollment_checklist.guardian == YES and not self.guardian_name:
            raise ConsentValidationError(
                'Expected guardian name. See {}.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'guardian_name')
        elif enrollment_checklist.guardian in [NO, NOT_APPLICABLE] and self.guardian_name:
            raise ConsentValidationError(
                'Guardian name not expected. See {}.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'guardian_name')
        # match citizenship
        if enrollment_checklist.citizen != self.citizen:
            raise ConsentValidationError(
                'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'citizen')
        # match literacy
        if enrollment_checklist.literacy == YES and self.is_literate != YES:
            raise ConsentValidationError(
                'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'is_literate')
        elif enrollment_checklist.literacy == NO and self.is_literate != NO:
            raise ConsentValidationError(
                'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name), 'is_literate')
        elif enrollment_checklist.literacy == NO and self.is_literate == NO and not self.witness_name:
            raise ConsentValidationError('Witness name is required', 'witness_name')
        # match marriage if not citizen
        if self.citizen == NO:
            if (enrollment_checklist.legal_marriage != self.legal_marriage) or (
                    enrollment_checklist.marriage_certificate != self.marriage_certificate):
                raise ConsentValidationError(
                    'Citizenship by marriage mismatch. {} reports subject is married '
                    'to a citizen with a valid marriage certificate. This does not match \'{}\''.format(
                        self._meta.verbose_name,
                        EnrollmentChecklist._meta.verbose_name))
        super().common_clean()

    @property
    def common_clean_exceptions(self):
        return super().common_clean_exceptions + [ConsentValidationError, AgeValueError]

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
