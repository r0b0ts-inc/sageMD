import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from string import punctuation

# After writing the code below, go to your settings.py and  update the AUTH_PASSWORD_VALIDATORS


class NumberValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_digits:
            raise ValidationError(
                _("Password must contain at least %(min_digits)d digit(s), 0-9"),
                code='password_no_number', 
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return _("Password must contain at least %(min_digits)d digit(s), 0-9" % {'min_digits': self.min_digits})


class UpperCaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least 1 upper case letter, A-Z"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Password must contain at least 1 upper case letter, A-Z")


class LowerCaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("Password must contain at least 1 lower case letter, a-z"),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _("Password must contain at least 1 lower case letter, a-z")


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall("['!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password):
            raise ValidationError(
                _("Password must contain at least 1 symbol character"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Password must contain at least 1 symbol character")
