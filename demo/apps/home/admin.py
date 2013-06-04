from django.contrib import admin
from django.contrib.auth.models import Group
from demo.apps.home.forms import ClienteCreationForm, ClienteChangeForm
from demo.apps.home.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    form = ClienteChangeForm
    add_form = ClienteCreationForm

    list_display = ('username','email','is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informacion Personal', {'fields': ('fecha_nacimiento',)}),
        ('Permisos', {'fields': ('is_admin',)}),
        (None, {'fields': ('last_login',)}),
    )
    search_fields = ('username','email')

admin.site.unregister(Group)
admin.site.register(Cliente,ClienteAdmin)