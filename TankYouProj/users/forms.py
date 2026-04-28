from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Fieldset
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellidos',
            'email',
            'dni',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'password',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'card p-4 shadow-sm'

        self.helper.layout = Layout(
            Fieldset(
                "👤 Datos personales",
                Row(
                    Column('nombre', css_class='col-md-6'),
                    Column('apellidos', css_class='col-md-6'),
                ),
                Row(
                    Column('dni', css_class='col-md-6'),
                    Column('fecha_nacimiento', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                "📧 Contacto",
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('telefono', css_class='col-md-6'),
                ),
                'direccion',
            ),
            Fieldset(
                "🔐 Seguridad",
                Column('password'),
            ),
            Submit('submit', 'Guardar usuario', css_class='btn btn-primary w-100 mt-3')
        )


class UsuarioUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label="Nueva contraseña (opcional)",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellidos',
            'email',
            'dni',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'is_active',
            'is_staff',
            'is_admin',
            'verificado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'card p-4 shadow-sm'

        self.helper.layout = Layout(
            Fieldset(
                "👤 Datos personales",
                Row(
                    Column('nombre', css_class='col-md-6'),
                    Column('apellidos', css_class='col-md-6'),
                ),
                Row(
                    Column('dni', css_class='col-md-6'),
                    Column('fecha_nacimiento', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                "📧 Contacto",
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('telefono', css_class='col-md-6'),
                ),
                'direccion',
            ),
            Fieldset(
                "Estado y permisos",
                'is_active',
                'verificado',
                'is_staff',
                'is_admin',
                'password',
            ),
            Submit('submit', 'Guardar cambios', css_class='btn btn-primary w-100 mt-3')
        )