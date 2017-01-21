from edc_metadata.rules.crf_rule import CrfRule
from edc_metadata.rules.decorators import register
from edc_metadata.rules.logic import Logic
from edc_metadata.rules.requisition_rule import RequisitionRule
from edc_metadata.rules.rule_group import RuleGroup
from edc_metadata.rules.predicate import P, PF

from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_constants.constants import NO, YES, POS, NEG, FEMALE, DWTA

from .constants import VENOUS
from .labs import microtube_panel, rdb_panel, viral_load_panel, elisa_panel, venous_panel
from .models import ResourceUtilization, SubjectVisit
from .rule_group_funcs import (
    func_art_naive_at_annual_or_defaulter,
    func_hiv_indeterminate_today,
    func_hiv_positive_today,
    func_hiv_untested,
    func_known_pos_in_prev_year,
    func_rbd,
    func_require_pima,
    func_circumcision_not_required,
    func_show_hic_enrollment,
    func_show_microtube,
    func_todays_hiv_result_required,
    func_vl,
    is_male,
    func_show_recent_partner,
    func_show_second_partner_forms,
    func_show_third_partner_forms)


@register()
class SubjectVisitRuleGroup(RuleGroup):

    gender_circumsion = CrfRule(
        logic=Logic(
            predicate=func_circumcision_not_required,
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['circumcision', 'circumcised', 'uncircumcised'])

    gender_menopause = CrfRule(
        logic=Logic(
            predicate=is_male,
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    known_pos_in_y1 = CrfRule(
        logic=Logic(
            predicate=func_known_pos_in_prev_year,
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['hivtestreview', 'hivtested', 'hivtestinghistory', 'hivresultdocumentation', 'hivresult', 'hivuntested'])

    pima_art_naive_enrollment_req_ahs = CrfRule(
        logic=Logic(
            predicate=func_require_pima,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['pima'])

    hiv_linkage_to_care_art_naive = CrfRule(
        logic=Logic(
            predicate=func_art_naive_at_annual_or_defaulter,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivlinkagetocare'])

    require_microtube = RequisitionRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[microtube_panel])

    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_vl,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[viral_load_panel], )

    rbd_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_rbd,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[rdb_panel], )

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = None
        source_model = 'bcpp_subject.subjectvisit'


@register()
class ResourceUtilizationRuleGroup(RuleGroup):

    out_patient = CrfRule(
        logic=Logic(
            # TODO: add back this PF('out_patient', lambda x: True if (x == NO or x == REFUSE) else False)
            predicate=P('out_patient', 'eq', NO),
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['bcpp_subject.outpatientcare'])

    hospitalized = CrfRule(
        logic=Logic(
            predicate=P('hospitalized', 'eq', 0),
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['bcpp_subject.hospitaladmission'])

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = (SubjectVisit, 'subject_visit')
        source_model = ResourceUtilization


@register()
class HivTestingHistoryRuleGroup(RuleGroup):

    has_record = CrfRule(
        logic=Logic(
            predicate=P('has_record', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivtestreview'])

    has_tested = CrfRule(
        logic=Logic(
            predicate=P('has_tested', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivtested'])

    hiv_untested = CrfRule(
        logic=Logic(
            predicate=func_hiv_untested,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivuntested'])

    other_record = CrfRule(
        logic=Logic(
            predicate=P('other_record', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivresultdocumentation'])

    require_todays_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivresult'])

    verbal_hiv_result_hiv_care_baseline = CrfRule(
        logic=Logic(
            predicate=P('verbal_hiv_result', 'eq', POS),
            consequence=REQUIRED,
            alternative=REQUIRED),
        target_models=['hivcareadherence', 'positiveparticipant', 'hivmedicalcare', 'hivhealthcarecosts'])

    verbal_response = CrfRule(
        logic=Logic(
            predicate=P('verbal_hiv_result', 'eq', NEG),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['stigma', 'stigmaopinion'])

#     other_response = CrfRule(
#         logic=Logic(
#             predicate=func_no_verbal_hiv_result,
#             consequence=REQUIRED,
#             alternative='do_nothing'),
#         target_models=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', 'stigma', 'stigmaopinion'])

    def method_result(self):
        return True

    class Meta:
        app_label = 'bcpp_subject'
        source_model = 'bcpp_subject.hivtestinghistory'


@register()
class ReviewPositiveRuleGroup(RuleGroup):

    recorded_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant'])

    recorded_hivresult = CrfRule(
        logic=Logic(
            predicate=P('recorded_hiv_result', 'eq', NEG),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['stigma', 'stigmaopinion'])

    require_todays_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_model = 'bcpp_subject.hivTestReview'


@register()
class HivCareAdherenceRuleGroup(RuleGroup):

    medical_care = CrfRule(
        logic=Logic(
            predicate=P('medical_care', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivmedicalcare'])

    pima_for_art_naive = CrfRule(
        logic=Logic(
            predicate=func_require_pima,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['pima'])

    require_todays_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_model = 'bcpp_subject.hivcareadherence'


@register()
class SexualBehaviourRuleGroup(RuleGroup):

    partners = CrfRule(
        logic=Logic(
            predicate=func_show_recent_partner,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['recentpartner'])

    last_year_partners = CrfRule(
        logic=Logic(
            predicate=func_show_second_partner_forms,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['secondpartner'])

    more_partners = CrfRule(
        logic=Logic(
            predicate=func_show_third_partner_forms,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['thirdpartner'])

    ever_sex = CrfRule(
        logic=Logic(
            predicate=PF(
                'ever_sex', 'gender',
                func=lambda x, y: True if x == YES and y == FEMALE else False),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_model = 'bcpp_subject.sexualbehaviour'


@register()
class CircumcisionRuleGroup(RuleGroup):

    circumcised = CrfRule(
        logic=Logic(
            predicate=P('circumcised', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['circumcised'])

    uncircumcised = CrfRule(
        logic=Logic(
            predicate=P('circumcised', 'eq', NO),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['bcpp_subject.uncircumcised'])

    class Meta:
        app_label = 'bcpp_subject'
        source_model = 'bcpp_subject.circumcision'


@register()
class ReproductiveRuleGroup(RuleGroup):

    currently_pregnant = CrfRule(
        logic=Logic(
            # TODO: verify this is correct
            predicate=PF(
                'currently_pregnant', 'menopause',
                func=lambda x, y: True if x == YES or y == YES else False),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['bcpp_subject.pregnancy'])

    non_pregnant = CrfRule(
        logic=Logic(
            # TODO: verify this is correct
            # predicate=PF(('currently_pregnant', 'eq', 'No'),
            #    ('menopause', 'eq', 'No', 'and')), TODO: Convert to func
            predicate=PF(
                'currently_pregnant', 'menopause',
                func=lambda x, y: True if x == NO and y == NO else False),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['bcpp_subject.nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        # source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.reproductivehealth'


@register()
class MedicalDiagnosesRuleGroup(RuleGroup):
    """"Allows the heartattack, cancer, tb forms to be made available whether or not the participant
    has a record. see redmine 314."""
    heart_attack_record = CrfRule(
        logic=Logic(
            predicate=P('heart_attack_record', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['heartattack'])

    cancer_record = CrfRule(
        logic=Logic(
            predicate=P('cancer_record', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['cancer'])

    tb_record_tubercolosis = CrfRule(
        logic=Logic(
            predicate=P('tb_record', 'eq', YES),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['tubercolosis'])

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.medicaldiagnoses'


class BaseRequisitionRuleGroup(RuleGroup):
    """Ensures an RBD requisition if HIV result is POS."""
    rbd_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_rbd,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[rdb_panel], )

    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_vl,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[viral_load_panel], )

    """Ensures a Microtube is not required for POS."""
    microtube_for_neg = RequisitionRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[microtube_panel], )

    pima_for_art_naive = CrfRule(
        logic=Logic(
            predicate=func_require_pima,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['pima'])

    hic = CrfRule(
        logic=Logic(
            predicate=func_show_hic_enrollment,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['hicenrollment'])

    class Meta:
        abstract = True


@register()
class RequisitionRuleGroup1(BaseRequisitionRuleGroup):

    """Ensures an ELISA blood draw requisition if HIV result is IND."""
    elisa_for_ind = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[elisa_panel, ], )

    """Ensures a venous blood draw requisition is required if insufficient
    volume in the capillary (microtube)."""
    venous_for_vol = RequisitionRule(
        logic=Logic(
            predicate=PF(
                'insufficient_vol', 'blood_draw_type',
                func=lambda x, y: True if x == YES or y == VENOUS else False),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_model='bcpp_subject.subjectrequisition',
        target_panels=[venous_panel], )

    serve_sti_form = CrfRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['bcpp_subject.sti'])

    elisa_result = CrfRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['bcpp_subject.elisahivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.hivresult'


@register()
class RequisitionRuleGroup2(BaseRequisitionRuleGroup):

    serve_hiv_care_adherence = CrfRule(
        logic=Logic(
            predicate=PF(
                'has_tested', 'verbal_hiv_result',
                func=lambda y, x: True if x == NEG or y == DWTA else False),
            consequence=NOT_REQUIRED,
            alternative=REQUIRED),
        target_models=['hivcareadherence', 'hivmedicalcare'])

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.hivtestinghistory'


@register()
class RequisitionRuleGroup3(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.hivtestreview'


@register()
class RequisitionRuleGroup4(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.hivresultdocumentation'


@register()
class RequisitionRuleGroup5(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        #  source_fk = (SubjectVisit, 'subject_visit')
        source_model = 'bcpp_subject.elisahivresult'
