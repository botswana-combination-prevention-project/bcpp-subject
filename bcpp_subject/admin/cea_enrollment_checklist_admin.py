from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import CeaEnrollmentChecklist
from ..forms import CeaEnrollmentChecklistForm

from .modeladmin_mixins import ModelAdminMixin


@admin.register(CeaEnrollmentChecklist, site=bcpp_subject_admin)
class CeaEnrollmentChecklistAdmin(ModelAdminMixin):

    form = CeaEnrollmentChecklistForm
    fieldsets = (
        (None, {
            'fields': [
                'registered_subject',
                'report_datetime',
                'citizen',
                'legal_marriage',
                'marriage_certificate',
                'marriage_certificate_no',
                'community_resident',
                'enrollment_reason',
                'cd4_date',
                'cd4_count',
                'opportunistic_illness',
                'diagnosis_date',
                'date_signed',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'citizen': admin.VERTICAL,
        'legal_marriage': admin.VERTICAL,
        'marriage_certificate': admin.VERTICAL,
        'community_resident': admin.VERTICAL,
        'enrollment_reason': admin.VERTICAL,
        'opportunistic_illness': admin.VERTICAL, }
