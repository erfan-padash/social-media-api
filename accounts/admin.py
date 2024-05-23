from django.contrib import admin
from .models import Account, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    list_per_page = 20
    readonly_fields = ('is_active', 'is_admin', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('permissions', {'fields': ('is_admin', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'last_login')})
    )

    add_fieldsets = (
        ('Make User', {'fields': ('phone_number', 'full_name', 'email', 'password1', 'password2')}),
    )

    search_fields = ('phone_number', 'email')
    filter_horizontal = ('groups', 'user_permissions')
    ordering = ('full_name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('account_name', 'user', )
    list_filter = ('user',)
    list_per_page = 20

