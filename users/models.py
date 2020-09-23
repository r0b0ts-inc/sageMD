from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.functions import Length
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save
from phonenumber_field.modelfields import PhoneNumberField

from allauth.account.models import EmailAddress

from .managers import CustomUserManager

# Create your models here.
class BaseUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, validators=[validate_email])
    password = models.CharField(max_length=128)
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
        null=True
    )

    EMAIL_FIELD = 'email'
    # USERNAME_FIELD = None
    REQUIRED_FIELDS = ['email', ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'SageMD Base User'

    def __str__(self):
        return str(self.email)


@receiver(post_save, sender=BaseUser)
def auto_create_profile_and_wallet_on_signup(sender, instance, *args, **kwargs):
    """This also handles username change automatically in wallet on username update in Iwise User"""
    Profile.objects.update_or_create(user=instance)

    if instance.is_superuser:
        """Create an allauth email address object for the superuser to login with from the front end"""
        EmailAddress.objects.update_or_create(
            user=instance,
            defaults={
                'email': instance.email, 
                'verified': True, 
                'primary': True
            }
        )


class Profile(models.Model):
    base_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    phone_number = PhoneNumberField(unique=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email()} {profile}"
