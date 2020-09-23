from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator

custom_username_validator = [UnicodeUsernameValidator(), ASCIIUsernameValidator()]
