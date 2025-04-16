from django.utils.translation import gettext_lazy as _
from base.choices import ChoicesEnum

class MedicalRecordStatusChoices(ChoicesEnum):
    """
    Status choices specific to medical records
    """
    DRAFT = ('draft', _('Draft'))
    PENDING_REVIEW = ('pending_review', _('Pending Review'))
    REVIEWED = ('reviewed', _('Reviewed'))
    ACTIVE = ('active', _('Active'))
    INACTIVE = ('inactive', _('Inactive'))
    ARCHIVED = ('archived', _('Archived'))

class BloodGroupChoices(ChoicesEnum):
    """
    Blood group choices
    """
    A_POSITIVE = ('A+', _('A+'))
    A_NEGATIVE = ('A-', _('A-'))
    B_POSITIVE = ('B+', _('B+'))
    B_NEGATIVE = ('B-', _('B-'))
    O_POSITIVE = ('O+', _('O+'))
    O_NEGATIVE = ('O-', _('O-'))
    AB_POSITIVE = ('AB+', _('AB+'))
    AB_NEGATIVE = ('AB-', _('AB-'))

class RecordTypeChoices(ChoicesEnum):
    """
    Types of medical records
    """
    GENERAL = ('general', _('General'))
    CONSULTATION = ('consultation', _('Consultation'))
    LAB_RESULT = ('lab_result', _('Laboratory Result'))
    PRESCRIPTION = ('prescription', _('Prescription'))
    SURGERY = ('surgery', _('Surgery'))
    VACCINATION = ('vaccination', _('Vaccination'))
    IMAGING = ('imaging', _('Imaging')) 