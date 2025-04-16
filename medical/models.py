from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from base.models import BaseModel, StatusModel
from base.choices import ChoiceField
from .choices import MedicalRecordStatusChoices, RecordTypeChoices

class MedicalRecord(BaseModel, StatusModel):
    """
    A model for storing patient medical records with status tracking.
    """
    # Override the status field with medical-specific choices
    status = ChoiceField(
        MedicalRecordStatusChoices,
        default=MedicalRecordStatusChoices.DRAFT.value,
        verbose_name=_('Status')
    )
    
    # Record type
    record_type = ChoiceField(
        RecordTypeChoices,
        default=RecordTypeChoices.GENERAL.value,
        verbose_name=_('Record Type')
    )
    
    # Patient this record belongs to
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name=_('Patient')
    )
    
    # Doctor who created/updated this record
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_records',
        verbose_name=_('Doctor')
    )
    
    # Record details
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    diagnosis = models.TextField(verbose_name=_('Diagnosis'), blank=True, null=True)
    prescription = models.TextField(verbose_name=_('Prescription'), blank=True, null=True)
    
    # Record date
    record_date = models.DateField(verbose_name=_('Record Date'))
    
    # Follow-up information
    follow_up_required = models.BooleanField(default=False, verbose_name=_('Follow-up Required'))
    follow_up_date = models.DateField(null=True, blank=True, verbose_name=_('Follow-up Date'))
    
    # Attachments
    attachments = models.FileField(
        upload_to='medical_records/',
        null=True,
        blank=True,
        verbose_name=_('Attachments')
    )
    
    class Meta:
        verbose_name = _('Medical Record')
        verbose_name_plural = _('Medical Records')
        ordering = ['-record_date', '-created_at']
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.title} ({self.get_status_display()})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('medical:record_detail', args=[str(self.id)])
    
    def mark_as_reviewed(self, user=None):
        """Helper method to mark a record as reviewed"""
        self.change_status(MedicalRecordStatusChoices.REVIEWED, user)
    
    def mark_as_active(self, user=None):
        """Helper method to mark a record as active"""
        self.change_status(MedicalRecordStatusChoices.ACTIVE, user)
    
    def archive_record(self, user=None):
        """Helper method to archive a record"""
        self.change_status(MedicalRecordStatusChoices.ARCHIVED, user)
