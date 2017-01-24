from django.contrib import admin
from django.utils.translation import ugettext as _

from edc_base.fieldsets import Remove

from ..admin_site import bcpp_subject_admin
from ..forms import ResidencyMobilityForm
from ..models import ResidencyMobility
from ..constants import E0
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ResidencyMobility, site=bcpp_subject_admin)
class ResidencyMobilityAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ResidencyMobilityForm

    conditional_fieldlist = {
        E0: Remove(['intend_residency']),
    }

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'length_residence',
                'permanent_resident',
                'intend_residency',
                'nights_away',
                'cattle_postlands',
                'cattle_postlands_other')}),
    )

    radio_fields = {
        "length_residence": admin.VERTICAL,
        "permanent_resident": admin.VERTICAL,
        "intend_residency": admin.VERTICAL,
        "nights_away": admin.VERTICAL,
        "cattle_postlands": admin.VERTICAL}

    instructions = [
        _("<H5>Read to Participant</H5> <p>To start, I will be asking"
          " you some questions about yourself, your living"
          " situation, and about the people that you live with."
          " Your answers are very important to our research and"
          " will help us understand how to develop better health"
          " programs in your community. Some of these questions"
          " may be embarrassing and make you feel uncomfortable;"
          " however, it is really important that you give the most"
          " honest answer that you can. Please remember that all of "
          " your answers are confidential. If you do not wish to "
          " answer, you can skip any question.</p>")]
