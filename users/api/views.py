from allauth.account.utils import send_email_confirmation
from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView, LogoutView
from django.contrib.auth import get_user_model
from rest_framework import status, generics, exceptions
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from allauth.account.models import EmailAddress
from django.utils.translation import ugettext_lazy as _

from .permissions import IsProfileOwner
from .serializers import ChangeEmailSerializer, UserActivateSerializer, \
    UserActivateConfirmSerializer, ResetPasswordSerializer, ResendEmailConfirmationSerializer, UserProfileSerializer
from ..models import Profile

UserModel = get_user_model()


class LogoutView(LogoutView):
    """View only accessible to logged in users and invalidates token on POST request"""
    permission_classes = (IsAuthenticated, )


class ChangeEmailView(generics.CreateAPIView):
    """Allows authenticated users to be able to change their primary email address and replace the old email"""
    serializer_class = ChangeEmailSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Creates and replace a new email once confirmed for request.user"""
        user = self.request.user
        new_email = serializer.validated_data.get('email')
        EmailAddress.objects.get(user=user).change(self.request, new_email, confirm=True)


class UserActivateView(PasswordResetView):
    """Allows a user that has performed a delete profile method to reactivate their account again upon resetting
    their password with their registered email on the platform"""
    serializer_class = UserActivateSerializer

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent for your account activation")},
            status=status.HTTP_200_OK
        )


class UserActivateConfirmView(PasswordResetConfirmView):
    """This view changes the users is_active property to True upon the password reset is confirmed"""
    serializer_class = UserActivateConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("User has been activated successfully.")}
        )


class ResetPasswordView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    # Return the success message with OK HTTP status:
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class ResendEmailConfirmationView(GenericAPIView):
    """This view allows for resending another account confirmation email if the user fails to confirm their account
    upon signup"""
    permission_classes = [AllowAny, ]
    serializer_class = ResendEmailConfirmationSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response({
                'message': 'This email is already verified'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response({
                    'message': 'Email confirmation sent Again'
                }, status=status.HTTP_201_CREATED)
            except APIException:
                return Response({
                    'message': 'This email does not exist, please create a new account'
                }, status=status.HTTP_403_FORBIDDEN)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """email, points and pk are read only field, all other fields can be updated"""
    permission_classes = (IsAuthenticated, IsProfileOwner, )
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'User Profile Detail'

    def get_object(self):
        obj = get_object_or_404(Profile, user__username=self.kwargs['username'])
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response({
                'message': 'PUT method not allowed for this view'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        request.user.is_active = None
        request.user.save()
        return Response({
            'message': 'This account has been inactivated successfully'
        }, status=status.HTTP_204_NO_CONTENT)
