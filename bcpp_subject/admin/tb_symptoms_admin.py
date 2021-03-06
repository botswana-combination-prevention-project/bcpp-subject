from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import TbSymptomsForm
from ..models import TbSymptoms
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbSymptoms, site=bcpp_subject_admin)
class TbSymptomsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbSymptomsForm

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'cough',
                'fever',
                'lymph_nodes',
                'cough_blood',
                'night_sweat',
                'weight_loss')
        }),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "cough": admin.VERTICAL,
        "fever": admin.VERTICAL,
        "lymph_nodes": admin.VERTICAL,
        "night_sweat": admin.VERTICAL,
        "weight_loss": admin.VERTICAL,
        "cough_blood": admin.VERTICAL, }
