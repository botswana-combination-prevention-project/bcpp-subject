from edc_appointment.managers import AppointmentManager
from edc_base.model.models import HistoricalRecords, BaseUuidModel
from edc_appointment.model_mixins import AppointmentModelMixin
from survey.model_mixins import SurveyModelMixin


class Appointment(AppointmentModelMixin, SurveyModelMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    objects = AppointmentManager()

    history = HistoricalRecords()

    class Meta(AppointmentModelMixin.Meta):
        app_label = 'bcpp_subject'
