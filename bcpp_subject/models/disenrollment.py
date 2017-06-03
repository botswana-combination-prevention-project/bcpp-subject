from edc_base.model_mixins import BaseUuidModel
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin

from ..managers import DisenrollmentManager

from .requires_consent_model_mixin import RequiresConsentMixin


class DisenrollmentBhs(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    objects = DisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'visit_schedule_bhs.bhs_schedule'
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'


class DisenrollmentAhs(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    objects = DisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'visit_schedule_ahs.ahs_schedule'
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'


class DisenrollmentEss(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    objects = DisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'visit_schedule_ess.ess_schedule'
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'


class DisenrollmentAno(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    objects = DisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'visit_schedule_ano.ano_schedule'
        consent_model = 'bcpp_subject.anonymousconsent'
        app_label = 'bcpp_subject'
