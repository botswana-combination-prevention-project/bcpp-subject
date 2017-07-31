from bcpp_subject_form_validators import SexualPartnerFormValidator as BaseFormValidator
from ..models import SecondPartner
from .form_mixins import SubjectModelFormMixin


class SexualPartnerFormValidator(BaseFormValidator):
    sexual_behaviour_model = 'bcpp_subject.sexualbehaviour'
    partner_residency_model = 'bcpp_subject.partnerresidency'


class SecondPartnerForm(SubjectModelFormMixin):

    form_validator_cls = SexualPartnerFormValidator

    class Meta:
        model = SecondPartner
        fields = '__all__'
