import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from ...models import SubjectConsent
from ..wrappers import SubjectConsentModelWrapper
from .base_listboard import BaseListboardView
from edc_map.models import InnerContainer


class ListboardView(BaseListboardView):

    model = SubjectConsent
    model_wrapper_class = SubjectConsentModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_exclude_options(self, request, *args, **kwargs):
        options = super().get_queryset_exclude_options(
            request, *args, **kwargs)
        plot_identifier = django_apps.get_app_config(
            'plot').anonymous_plot_identifier
        options.update(
            {'household_member__household_structure__household__plot__plot_identifier': plot_identifier})
        return options

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        plot_identifier_list = []
        try:
            plot_identifier_list = InnerContainer.objects.get(
                username=request.user.username).identifier_labels
        except InnerContainer.DoesNotExist:
            plot_identifier_list = []
        if plot_identifier_list:
            options.update(
                {'household_member__household_structure__household__plot__plot_identifier__in': plot_identifier_list})
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        if kwargs.get('survey_schedule'):
            options.update(
                {'survey_schedule': kwargs.get('survey_schedule')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
