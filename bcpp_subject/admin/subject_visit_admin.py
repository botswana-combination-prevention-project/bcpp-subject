from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from member.models import HouseholdMember

from ..admin_site import bcpp_subject_admin
from ..forms import SubjectVisitForm
from ..models import SubjectVisit, SubjectRequisition

from .modeladmin_mixins import ModelAdminMixin


@admin.register(SubjectVisit, site=bcpp_subject_admin)
class SubjectVisitAdmin(VisitModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):

    form = SubjectVisitForm

    requisition_model = SubjectRequisition

    list_display = (
        'appointment',
        'report_datetime',
        'reason',
        "info_source",
        'created',
        'user_created',
    )

    list_filter = (
        'report_datetime',
        'reason',
        'household_member__household_structure__household__plot__map_area',
        'appointment__appt_status',
        'appointment__visit_code',
    )

    search_fields = (
        'appointment__subject_identifier',
        'appointment__registered_subject__registration_identifier',
        'appointment__registered_subject__first_name',
        'appointment__registered_subject__identity',
    )

    fields = (
        'household_member',
        "appointment",
        "report_datetime",
        "comments"
    )

    def view_on_site(self, obj):
        try:
            return reverse(
                'bcpp-subject:dashboard_url', kwargs=dict(
                    household_identifier=obj.household_member.household_structure.household.household_identifier,
                    subject_identifier=obj.subject_identifier,
                    appointment=str(obj.appointment.id),
                    survey=obj.survey,
                    survey_schedule=obj.survey_schedule_object.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = HouseholdMember.objects.none()
            if HouseholdMember.objects.filter(id=request.GET.get('household_member')):
                household_members = HouseholdMember.objects.filter(id=request.GET.get('household_member'))
            kwargs["queryset"] = household_members
        return super(SubjectVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
