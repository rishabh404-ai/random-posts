from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','username','full_name','is_verified','is_active','is_staff','created_at','updated_at','is_superuser')
    list_filter = ('id','email','username','firstname','lastname','is_verified','is_active','is_staff','created_at','updated_at','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password','username','firstname','lastname')}),
        ('Permissions', {'fields': ('is_staff', 'is_verified', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('id','email','username','firstname','lastname','is_verified','is_active','is_staff','created_at','updated_at','is_superuser')
    ordering = ('email','username')
    filter_horizontal = ()

  
admin.site.register(User, UserAdmin)
