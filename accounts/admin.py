from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff','groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture','joining_date')}),
        ('Permissions', {'fields': ('is_active', 'is_admin','is_staff', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','first_name', 'last_name', 'phone_number')}
        ),
    )
    search_fields = ('email', 'username', 'phone_number', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ()

    readonly_fields = [
        'password',
        'joining_date',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_admin = request.user.is_admin
        disabled_fields = set()

        if not is_admin:
            disabled_fields |= {
                'is_active',
                'is_admin',
                'is_staff',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
    
    def has_add_permission(self, request, obj=None):
        return True


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)