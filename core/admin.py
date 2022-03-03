from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# "as _": this is a recommended convention for converting strings in our Python to human readable text.
# and the reason is it gets passed through the translation engine.
from django.utils.translation import gettext as _

from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # Fieldsets: are showed in the admin panel when changing user model or creating it.
    fieldsets = (
        # define the sections for fieldsets in our change and create page.
        # title of the section, it contains fields.
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            { 'fields': ('is_active', 'is_staff', 'is_superuser') }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    # the user admin, by default, takes an "add_fieldsets" which defines the fields that you include on the add page.
    # Customizing this fieldset to include (email, password, password2)
    # So you can create a new user in the system with a very minimal data that's required.
    # And if you want to add extra fields like the name and customize that stuff later in the Edit page.
    add_fieldsets = (
        (None, {
            # "classes": are assigned to the form and taking the defaults from the user admin documentation
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
