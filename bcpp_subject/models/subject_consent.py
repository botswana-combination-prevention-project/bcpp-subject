import re
import uuid

from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.model_managers import HistoricalRecords
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
    SampleCollectionFieldsMixin, CitizenFieldsMixin)
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO
from edc_search.model_mixins import SearchSlugManager
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_map.site_mappers import site_mappers
from edc_registration.exceptions import RegisteredSubjectError
from edc_registration.models import RegisteredSubject
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin
    as BaseUpdatesOrCreatesRegistrationModelMixin)

from member.models import HouseholdMember
from survey.model_mixins import SurveyScheduleModelMixin

from ..managers import SubjectConsentManager
from ..patterns import subject_identifier
from .model_mixins import SearchSlugModelMixin
from .utils import is_minor
from ..utils import rbd_household_member


class Manager(SubjectConsentManager, SearchSlugManager):
    pass


class UpdatesOrCreatesRegistrationModelMixin(BaseUpdatesOrCreatesRegistrationModelMixin):

    @property
    def registration_options(self):
        """Insert internal_identifier to be updated on
        RegisteredSubject.
        """
        registration_options = super().registration_options
        registration_options.update(
            registration_identifier=self.household_member.internal_identifier.hex)
        return registration_options

    def registration_raise_on_illegal_value_change(self, registered_subject):
        """Raises an exception if a value changes between
        updates.
        """
        if registered_subject.identity != self.identity:
            raise RegisteredSubjectError(
                'Identity may not be changed. Expected {}. Got {}'.format(
                    registered_subject.identity,
                    self.identity))
        if (registered_subject.registration_identifier
            and uuid.UUID(registered_subject.registration_identifier) != 
                self.household_member.internal_identifier):
            raise RegisteredSubjectError(
                'Internal Identifier may not be changed. Expected {}. '
                'Got {}'.format(
                    registered_subject.registration_identifier,
                    self.household_member.internal_identifier))
        if registered_subject.dob != self.dob:
            raise RegisteredSubjectError(
                'DoB may not be changed. Expected {}. Got {}'.format(
                    registered_subject.dob,
                    self.dob))

    class Meta:
        abstract = True


class SubjectConsent(
        ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin, SurveyScheduleModelMixin,
        IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
        SampleCollectionFieldsMixin, CitizenFieldsMixin,
        VulnerabilityFieldsMixin, SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the user that captures the ICF.
    """

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=('Subject is a minor if aged 16-17. A guardian must '
                   'be present for consent. HIV status may NOT be '
                   'revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(
        default=False,
        editable=False)

    objects = Manager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return '{0} ({1}) V{2}'.format(
            self.subject_identifier,
            self.survey_schedule_object.name,
            self.version)

    def save(self, *args, **kwargs):
        existing_rbd_household_member = rbd_household_member(
            identity=self.identity)
        household_member = self.household_member
        if existing_rbd_household_member:
            try:
                registered_subject = RegisteredSubject.objects.get(
                    identity=self.identity)
            except RegisteredSubject.DoesNotExist as e:
                raise RegisteredSubjectError(
                    f'{RegisteredSubject._meta.verbose_name} should exist. '
                    f'Got {e}') from e
            household_member.internal_identifier = existing_rbd_household_member.internal_identifier
            household_member.save()
            self.subject_identifier = registered_subject.subject_identifier
            household_member = HouseholdMember.objects.get(
                id=household_member.id)
            self.household_member = household_member
        if not self.id:
            self.survey_schedule = self.household_member.survey_schedule_object.field_value
            if re.match(subject_identifier, self.household_member.subject_identifier):
                self.subject_identifier = self.household_member.subject_identifier
        self.study_site = site_mappers.current_map_code
        self.is_minor = YES if is_minor(
            self.dob, self.consent_datetime) else NO
        super().save(*args, **kwargs)

    def natural_key(self):
        return ((self.subject_identifier, self.version,) + 
                self.household_member.natural_key())
    natural_key.dependencies = ['bcpp_subject.household_member']

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created',)
