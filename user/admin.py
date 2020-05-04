from django.contrib import admin
from django import forms
from .models import User

class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'email', 'mobile', 'password', 'avatar']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'email', 'mobile', 'password', 'avatar']

admin.site.register(User, UserAdmin)


