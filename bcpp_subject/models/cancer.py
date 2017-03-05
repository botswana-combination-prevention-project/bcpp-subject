from django.db import models

from edc_base.model_validators import date_not_future
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords

from ..choices import DXCANCER_CHOICE

from .model_mixins import CrfModelMixin, CrfModelManager


class Cancer (CrfModelMixin):

    """A model completed by the user to record any diagnosis of cancer in the past 12 months."""

    cancer_date = models.DateField(
        verbose_name="Date of the diagnosis of cancer:",
        validators=[date_not_future],
        help_text="")

    cancer_dx = models.CharField(
        verbose_name="[Interviewer:] What is the cancer diagnosis as recorded?",
        max_length=45,
        choices=DXCANCER_CHOICE,
        help_text="")

    cancer_dx_other = OtherCharField()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Cancer"
        verbose_name_plural = "Cancer"
