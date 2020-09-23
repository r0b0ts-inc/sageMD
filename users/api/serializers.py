import datetime

from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import *
from dj_rest_auth.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from . forms import UserActivateForm, ResetPasswordForm

from dj_rest_auth.serializers import LoginSerializer

from ..models import Profile

UserModel = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if app_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(_("Email already exists"))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_('Password must match'))
        return data

    def get_cleaned_user_data(self):
        return {
            'email': self.validated_data.get('email'),
            'password1': self.validated_data.get('password1'),
            'password2': self.validated_data.get('password2'),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_user_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class ChangeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', )


class UserActivateSerializer(PasswordResetSerializer):
    password_reset_form_class = UserActivateForm


class UserActivateConfirmSerializer(PasswordResetConfirmSerializer):
    def validate(self, attrs):
        super(UserActivateConfirmSerializer, self).validate(attrs)
        self.user.is_active = True
        self.user.save()
        return attrs


class ResetPasswordSerializer(PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm


class ResendEmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', )


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})
    email = None

    def validate(self, attrs):
        username = attrs.get('username')
        if username.startswith('+'):
            try:
                q = UserModel.objects.filter(phone_number=username)
                if q.exists():
                    attrs["username"] = q[0].username
            except UserModel.DoesNotExist:
                return None
        return super(CustomLoginSerializer, self).validate(attrs)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('pk', 'email', 'created_at')
        read_only_fields = ('email',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = PhoneNumberField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def validate_date_of_birth(self, value_of_date):
        today = datetime.date.today()
        age = relativedelta(today, value_of_date)
        if age.years < 18:
            raise serializers.ValidationError(_("You must be 18 years and above to sign up on this site"))
        return value_of_date
    
    def get_fields(self):
        fields = super(UserProfileSerializer, self).get_fields()
        try:
            if self.instance and self.instance.user:
                fields['user'].instance = self.instance.user
        except UserModel.DoesNotExist:
            pass
        return fields

    def update(self, instance, validated_data):
        clean_data = validated_data.pop('user')
        instance.phone_number = clean_data.get('phone_number', user.phone_number)
        instance.first_name = clean_data.get('first_name', user.first_name)
        instance.last_name = clean_data.get('last_name', user.last_name)
        instance.date_of_birth = clean_data.get('date_of_birth', user.date_of_birth)
        instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ('base_user', 'first_name', 'last_name', 'phone_number', 'date_of_birth',)

    