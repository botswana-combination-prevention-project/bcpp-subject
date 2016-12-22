from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import HistoricalRecords
from edc_constants.constants import YES

from ..choices import PLACE_CIRC, WHYCIRC_CHOICE, TIME_UNIT_CHOICE
from ..exceptions import CircumcisionError

from .model_mixins import CrfModelMixin, CrfModelManager, CircumcisionModelMixin


class Circumcised (CircumcisionModelMixin, CrfModelMixin):

    circ_date = models.DateField(
        verbose_name='When were you circumcised?',
        null=True,
        blank=True,)

    when_circ = models.IntegerField(
        verbose_name="At what age were you circumcised?",
        null=True,
        blank=True,
        help_text="Note: Leave blank if participant does not want to respond.")

    age_unit_circ = models.CharField(
        verbose_name="The unit of age of circumcision is?",
        max_length=25,
        choices=TIME_UNIT_CHOICE,
        null=True,
        blank=True,
        help_text="",
    )

    where_circ = models.CharField(
        verbose_name="Where were you circumcised?",
        max_length=45,
        choices=PLACE_CIRC,
        null=True,
        help_text="")

    where_circ_other = OtherCharField(
        null=True)

    why_circ = models.CharField(
        verbose_name="What was the main reason why you were circumcised?",
        max_length=55,
        choices=WHYCIRC_CHOICE,
        null=True,
        help_text="")

    why_circ_other = OtherCharField(
        null=True)

    objects = CrfModelManager()

    history = HistoricalRecords()

    def common_clean(self):
        if self.circumcised == YES and not self.health_benefits_smc:
            raise CircumcisionError('if {}, what are the benefits of male circumcision?.'.format(self.circumcised))
        if self.when_circ and not self.age_unit_circ:
            raise CircumcisionError('If you answered age of circumcision then you must provide time units.')
        if not self.when_circ and self.age_unit_circ:
            raise CircumcisionError(
                'If you did not answer age of circumcision then you must not provide time units.')
        super().common_clean()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Circumcised"
        verbose_name_plural = "Circumcised"
