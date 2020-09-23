from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import BaseUserChangeForm, BaseUserCreationForm
from .models import BaseUser, Profile


# Register your models here.
class CustomBaseUserAccountAdmin(UserAdmin):
    add_form = BaseUserCreationForm
    form = BaseUserChangeForm
    model = BaseUser

    list_display = ('email', 'is_active',)
    list_filter = ('is_superuser', 'date_joined')
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # form for adding new user from the backend
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
         ),
    )

    # search_fields = ()
    ordering = ('email',)


admin.site.register(BaseUser, CustomBaseUserAccountAdmin)


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass

