from django.contrib import admin
from .models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    model = Usuario
    list_display = ('email', 'nombre', 'apellidos', 'is_admin', 'is_staff', 'is_active')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not change or 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Usuario, UsuarioAdmin)