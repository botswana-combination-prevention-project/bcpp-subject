from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import ListboardViewMixin

from survey import SurveyViewMixin

from .listboard_mixins import BcppSubjectFilteredListViewMixin, BcppSubjectSearchViewMixin
from .mixins import SubjectAppConfigViewMixin


class ListBoardView(EdcBaseViewMixin, ListboardViewMixin, SubjectAppConfigViewMixin,
                    BcppSubjectFilteredListViewMixin, BcppSubjectSearchViewMixin,
                    SurveyViewMixin, TemplateView, FormView):

    app_config_name = 'bcpp_subject'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            MALE=MALE,
            reference_datetime=get_utcnow(),
        )
        return context
