from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin

from ..choices import VISIT_UNSCHEDULED_REASON

from .appointment import Appointment


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, RequiresConsentMixin,
                   SurveyModelMixin, BaseUuidModel):

    """A model completed by the user that captures the covering information for the data collected
    for this timepoint/appointment, e.g.report_datetime."""

    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    household_member = models.ForeignKey(HouseholdMember, on_delete=models.PROTECT)

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON,
    )

    objects = VisitModelManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.survey = self.appointment.survey_object.field_value
        self.survey_schedule = self.appointment.survey_object.survey_schedule.field_value
        self.info_source = 'subject'
        self.reason = SCHEDULED
        super().save(*args, **kwargs)

    class Meta(VisitModelMixin.Meta):
        app_label = "bcpp_subject"
        consent_model = 'bcpp_subject.subjectconsent'
