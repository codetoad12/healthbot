from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum

class ChoiceField(models.CharField):
    """
    Custom field type for storing choices from Enum classes.
    """
    def __init__(self, enum_class, *args, **kwargs):
        if not issubclass(enum_class, ChoicesEnum):
            raise ValueError('enum_class must be a subclass of ChoicesEnum')
        
        kwargs['choices'] = enum_class.choices()
        kwargs['max_length'] = max(len(choice.value) for choice in enum_class)
        super().__init__(*args, **kwargs)

class ChoicesEnum(Enum):
    """
    Base Enum class for all choice enums.
    Provides helper methods for Django choice fields.
    """
    @classmethod
    def choices(cls):
        """Returns tuple of (value, label) pairs for Django choice fields"""
        return [(choice.value, choice.label) for choice in cls]

    @property
    def label(self):
        """Returns the translated label for this choice"""
        return self._label_

    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label_ = label
        return obj

class BaseStatusChoices(ChoicesEnum):
    """
    Base status choices that can be extended by other apps
    """
    DRAFT = ('draft', _('Draft'))
    ACTIVE = ('active', _('Active'))
    INACTIVE = ('inactive', _('Inactive'))
    ARCHIVED = ('archived', _('Archived'))

class YesNoChoices(ChoicesEnum):
    """
    Simple Yes/No choices
    """
    YES = ('yes', _('Yes'))
    NO = ('no', _('No'))

class GenderChoices(ChoicesEnum):
    """
    Gender choices
    """
    MALE = ('male', _('Male'))
    FEMALE = ('female', _('Female'))
    OTHER = ('other', _('Other'))
    PREFER_NOT_TO_SAY = ('prefer_not_to_say', _('Prefer not to say')) 