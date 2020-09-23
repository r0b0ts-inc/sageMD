from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field


class CustomUserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        return super(CustomUserAccountAdapter, self).save_user(request, user, form, commit=commit)
