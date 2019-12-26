from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def max_value(value):
    if value >= 10:
        raise ValidationError('Value should not be more than 10.')