from django.contrib import admin
from .models import Account, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
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
        ('permissions', {'fields': ('is_admin', 'is_active', 'last_login')})
    )

    add_fieldsets = (
        ('Make User', {'fields': ('phone_number', 'full_name', 'email', 'password1', 'password2')}),
    )

    search_fields = ('phone_number', 'email')
    filter_horizontal = ()
    ordering = ('full_name',)


admin.site.unregister(Group)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('account_name', 'user', )
    list_filter = ('user',)
    list_per_page = 20

