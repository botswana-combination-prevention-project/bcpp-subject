from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ..base import ListboardView as BaseListboardView, FilteredListViewMixin, SearchViewMixin


class ListboardView(FilteredListViewMixin, SearchViewMixin, BaseListboardView):

    navbar_item_selected = 'bcpp_subject'
    navbar_name = 'default'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def filtered_queryset(self):
        qs = super().filtered_queryset
        plot_identifier = django_apps.get_app_config(
            'plot').anonymous_plot_identifier
        return qs.exclude(
            **{'household_member__household_structure'
               '__household__plot__plot_identifier': plot_identifier}).order_by(
            self.filtered_queryset_ordering)

    def search_queryset(self, search_term, **kwargs):
        qs = super().search_queryset(search_term, **kwargs)
        plot_identifier = django_apps.get_app_config(
            'plot').anonymous_plot_identifier
        return qs.exclude(
            **{'household_member__household_structure'
               '__household__plot__plot_identifier': plot_identifier}).order_by(
            self.filtered_queryset_ordering)
