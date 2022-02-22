from django.contrib import admin
from rest_framework_simplejwt import token_blacklist
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'id', 'name', 'is_seller', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active', 'is_superuser')
    fieldsets = (
        ('Security information', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_seller')}),
        ('Important date', {'fields': ('last_update', 'last_login', 'register_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('-id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
