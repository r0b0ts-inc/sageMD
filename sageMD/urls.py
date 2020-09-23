from allauth.account.views import confirm_email
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView, PasswordChangeView, LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from users.api import views

schema_view = get_schema_view(
   openapi.Info(
      title="Iwise Finance",
      default_version='v1',
      description="API for managing all the Iwise Finance endpoints",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@iwise.ng"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # This above exposes 4 endpoints:
    # A JSON view of your API specification at /swagger.json
    # A YAML view of your API specification at /swagger.yaml
    # A swagger-ui view of your API specification at /swagger/
    # A ReDoc view of your API specification at /redoc/


    # API URLS
    path('api/v1/users/', include('users.urls')),

    # dj_rest-auth and simple-jwt configuration inclusive
    re_path(r'^api/v1/change_email/$', views.ChangeEmailView.as_view(), name='change_email'),
    re_path(r'^api/v1/logout/$', views.LogoutView.as_view(), name='rest_logout'),
    re_path(r'^api/v1/user/activate/$', views.UserActivateView.as_view(), name='user_activate'),
    re_path(r'^api/v1/user/activate/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.UserActivateConfirmView.as_view(), name='user_activation_confirm'),
    re_path(r'^api/v1/password/reset/$', views.ResetPasswordView.as_view(), name='rest_password_reset'),
    re_path(r'^api/v1/email-verify-again/$', views.ResendEmailConfirmationView.as_view(),
            name='verify_email_again'),

    re_path(r'^api/v1/', include('dj_rest_auth.urls')),
    re_path(r'^api/v1/signup/', include('dj_rest_auth.registration.urls'),
            name='rest_reg'),
    re_path(r'^api/v1/verify-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^api/v1/account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email,
            name='account_confirm_email'),
    re_path(r'^api/v1/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^api/v1/password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
    re_path(r'^api/v1/login/$', LoginView.as_view(), name='rest_login'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# This line below is here so that I can only serve my media files on my local machine only. In production, I have to
# serve media files from Nginx, Apache or CDN.
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
