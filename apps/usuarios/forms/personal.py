from django import forms
from apps.usuarios.models.personal import PersonalAdministrativo

class PersonalAdministrativoForm(forms.ModelForm):
    class Meta:
        model = PersonalAdministrativo
        fields = ['rol', 'nombres', 'apellidos', 'ci', 'direccion', 'telefono', 'fecha_nacimiento', 'archivo_documentacion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
