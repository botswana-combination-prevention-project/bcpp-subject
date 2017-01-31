from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..constants import ANNUAL, BASELINE
from ..forms import HivResultDocumentationForm
from ..models import HivResultDocumentation

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivResultDocumentation, site=bcpp_subject_admin)
class HivResultDocumentationAdmin (CrfModelAdminMixin, admin.ModelAdmin):

    form = HivResultDocumentationForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'result_date',
                'result_doc_type')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'result_doc_type': admin.VERTICAL, }

    instructions = {
        BASELINE: [("This section collects information on whether or not the"
                    " participant has either:"
                    " <ol><li>documentation of an HIV test result other than the"
                    " most recent HIV test (positive, negative, or "
                    " indeterminate) ; OR </li>"
                    " <li> documentation that supports a previous diagnosis of"
                    " HIV, if record of positive HIV test is not available.</li>"
                    "</ol> (baseline) ")],
        ANNUAL: [("This section collects information on whether or not the"
                  " participant has either:"
                  " <ol><li>documentation of an HIV test result other than the"
                  " most recent HIV test; OR</li>"
                  " <li>documentation that supports a previous diagnosis of"
                  " HIV, if record of positive HIV test is not available.</li></ol> (annual)")]
    }
