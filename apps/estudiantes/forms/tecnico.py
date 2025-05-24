from django import forms
from apps.estudiantes.models.estudiante import Estudiante

class EstudianteTecnicoForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [
            'nombres', 'apellidos', 'ci', 'fecha_nacimiento', 'direccion',
            'telefono', 'colegio_universidad', 'ocupacion', 'archivo_documentacion'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer archivo obligatorio
        self.fields['archivo_documentacion'].required = True
