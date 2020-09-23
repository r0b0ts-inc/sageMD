from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import BaseUser


class BaseUserCreationForm(UserCreationForm):
    """
    New user creation form in the Admin backend
    """

    class Meta(UserCreationForm):
        model = BaseUser
        fields = ['email', ]


class BaseUserChangeForm(UserChangeForm):
    """
        Update user form. Doesn't allow changing password in the Admin.
        """

    class Meta:
        model = BaseUser
        fields = ['email', ]
