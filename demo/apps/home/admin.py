#-*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from demo.apps.home.models import Cliente
from django.contrib.auth.admin import UserAdmin

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña",widget=forms.PasswordInput)
    class Meta:
        model = Cliente
        fields = ('email','username')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        cliente = super(UserCreationForm,self).save(commit=False)
        cliente.email = self.cleaned_data.get('email')
        cliente.set_password(self.cleaned_data.get('password2'))
        if commit:
            cliente.save()
        return cliente

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Cliente
    def clean_password(self):
        return self.initial['password']

class ClienteAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_filter = ('is_admin',)
    list_display = ('username','email','is_admin')
    fieldsets = (
        (None, {'fields': ('username','email', 'password','avatar')}),
        ('Informacion Personal', {'fields': ('nombre','apellidos','direccion','telefono','fecha_nacimiento',)}),
        ('Permisos', {'fields': ('is_admin',)}),
        (None, {'fields': ('last_login',)}),
    )
    search_fields = ('username','email')

admin.site.unregister(Group)
admin.site.register(Cliente,ClienteAdmin)