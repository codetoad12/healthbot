from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers import SoftDeleteManager
from .choices import ChoiceField, BaseStatusChoices

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_by` and `updated_by` fields.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name=_('Created by')
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name=_('Updated by')
    )

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    """
    An abstract base class model that provides soft-delete functionality
    with `is_deleted` and `deleted_at` fields.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_deleted',
        verbose_name=_('Deleted by')
    )

    # Use our custom manager
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Manager to get all objects including deleted ones

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()

class BaseModel(TimeStampedModel, UserStampedModel, SoftDeleteModel):
    """
    A base model that combines TimeStampedModel, UserStampedModel, and SoftDeleteModel.
    This is the main abstract model that other models should inherit from.
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from .middleware import get_current_user
        # If this is a new instance, set created_by
        if not self.pk and not self.created_by:
            self.created_by = get_current_user()
        # Always set updated_by
        self.updated_by = get_current_user()
        super().save(*args, **kwargs)

class StatusModel(models.Model):
    """
    An abstract base class model that provides status tracking
    with `status` and `status_changed_at` fields.
    """
    status = ChoiceField(
        BaseStatusChoices,
        default=BaseStatusChoices.DRAFT.value,
        verbose_name=_('Status')
    )
    status_changed_at = models.DateTimeField(null=True, blank=True)
    status_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_status_changed',
        verbose_name=_('Status changed by')
    )

    class Meta:
        abstract = True

    def change_status(self, new_status, user=None):
        from django.utils import timezone
        from .middleware import get_current_user
        
        # Handle both Enum members and string values
        status_value = new_status.value if hasattr(new_status, 'value') else new_status
        
        # Get the choices dict
        valid_choices = dict(self._meta.get_field('status').choices)
        
        if status_value in valid_choices:
            self.status = status_value
            self.status_changed_at = timezone.now()
            self.status_changed_by = user or get_current_user()
            self.save()
