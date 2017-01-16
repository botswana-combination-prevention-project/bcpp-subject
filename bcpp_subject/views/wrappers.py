from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_appointment.views import AppointmentModelWrapper
from edc_consent.views import ConsentModelWrapper
from edc_dashboard.wrappers.model_wrapper import ModelWrapper
from bcpp_subject.models.subject_visit import SubjectVisit


class ModelWrapperMixin(ModelWrapper):

    admin_site_name = django_apps.get_app_config('bcpp_subject').admin_site_name
    url_namespace = django_apps.get_app_config('bcpp_subject').url_namespace
    next_url_name = django_apps.get_app_config('bcpp_subject').dashboard_url_name

    extra_querystring_attrs = {}
    next_url_attrs = {'bcpp_subject.appointment': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = ['household_identifier', 'subject_identifier', 'survey_schedule', 'survey']

    def add_extra_attributes_after(self):
        super().add_extra_attributes_after()
        self.survey_object = self.wrapped_object.survey_object
        self.survey_schedule_object = self.wrapped_object.survey_schedule_object

    @property
    def members(self):
        return self.household_member.household_structure.householdmember_set.all()

    @property
    def plot_identifier(self):
        return self.household_member.household_structure.household.plot.plot_identifier

    @property
    def household_identifier(self):
        return self.household_member.household_structure.household.household_identifier

    @property
    def community_name(self):
        return self.survey_schedule_object.map_area_display


class VisitModelWrapper(ModelWrapperMixin):

    model_name = 'bcpp_subject.subjectvisit'
    extra_querystring_attrs = {
        'bcpp_subject.subjectvisit': [
            'appointment', 'household_member']}
    next_url_attrs = {'bcpp_subject.subjectvisit': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey',
        'appointment', 'household_member']


class AppointmentModelWrapper(AppointmentModelWrapper, ModelWrapperMixin):

    model_name = 'bcpp_subject.appointment'
    visit_model_wrapper_class = VisitModelWrapper

    @property
    def visit(self):
        try:
            return self.visit_model_wrapper_class(self._original_object.subjectvisit)
        except ObjectDoesNotExist:
            visit_model = django_apps.get_model(
                *self.visit_model_wrapper_class.model_name.split('.'))
            return self.visit_model_wrapper_class(
                visit_model(
                    household_member=self.household_member,
                    appointment=self._original_object,
                    subject_identifier=self.subject_identifier,
                    survey_schedule=self.survey_schedule_object.field_value,
                    survey=self.survey_object.field_value))


class ListBoardSubjectConsentModelWrapper(ConsentModelWrapper, ModelWrapperMixin):

    model_name = 'bcpp_subject.subjectconsent'
    next_url_name = django_apps.get_app_config('bcpp_subject').listboard_url_name


class DashboardSubjectConsentModelWrapper(ConsentModelWrapper, ModelWrapperMixin):

    next_url_name = django_apps.get_app_config('bcpp_subject').dashboard_url_name
    next_url_attrs = {'bcpp_subject.subjectconsent': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    extra_querystring_attrs = {
        'bcpp_subject.subjectconsent': ['gender', 'household_member', 'first_name', 'initials']}
    url_instance_attrs = [
        'subject_identifier', 'survey_schedule', 'survey', 'gender',
        'household_member', 'first_name', 'initials', 'household_identifier']
