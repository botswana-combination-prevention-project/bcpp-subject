import sys

from django.core.management.color import color_style

from edc_map.site_mappers import site_mappers
from edc_visit_schedule.visit_schedule import VisitSchedule

from .annual_schedule import annual_schedule
from .ess_schedule import ess_schedule

style = color_style()

try:
    map_area = site_mappers.current_map_area
except AttributeError as e:
    sys.stdout.write(style.ERROR(
        '  * ERROR: visit schedule requires the current map area. '
        'Either the site mapper is not set or the current map area '
        'is not a valid \'community\'.\n    Got {} ({})\n'.format(
            site_mappers.current_map_area, str(e))))


visit_schedule_annual = VisitSchedule(
    name='visit_schedule_annual',
    verbose_name='BCPP Visit Schedule Annual',
    app_label='bcpp_subject',
    default_enrollment_model='bcpp_subject.enrollment',
    default_disenrollment_model='bcpp_subject.disenrollment',
    visit_model='bcpp_subject.subjectvisit',
    offstudy_model='bcpp_subject.subjectoffstudy',
)


visit_schedule_ess = VisitSchedule(
    name='visit_schedule_ess',
    verbose_name='BCPP Visit Schedule ESS',
    app_label='bcpp_subject',
    default_enrollment_model='bcpp_subject.enrollmentess',
    default_disenrollment_model='bcpp_subject.disenrollmentess',
    visit_model='bcpp_subject.subjectvisit',
    offstudy_model='bcpp_subject.subjectoffstudy',
)

visit_schedule_annual.add_schedule(annual_schedule)
visit_schedule_ess.add_schedule(ess_schedule)
