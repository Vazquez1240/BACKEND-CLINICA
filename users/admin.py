from django.contrib import admin
from .models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as OriginalGroup

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_staff')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        if request.user.is_staff:
            return ('is_staff', 'groups', 'user_permissions')
        return super().get_readonly_fields(request, obj)

admin.site.register(Group)
admin.site.unregister(OriginalGroup)
