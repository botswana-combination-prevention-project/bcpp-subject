from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from edc_base.fieldsets import FieldsetsModelAdminMixin
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin,
                         FieldsetsModelAdminMixin, ModelAdminMixin):

    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. '
        'Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def view_on_site(self, obj):
        household_member = obj.subject_visit.household_member
        try:
            return reverse(
                'bcpp-subject:dashboard_url', kwargs=dict(
                    subject_identifier=household_member.subject_identifier,
                    household_identifier=(household_member.household_structure.
                                          household.household_identifier),
                    survey=obj.subject_visit.survey_object.field_value,
                    survey_schedule=obj.subject_visit.survey_schedule_object.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)
