from django import forms
from apps.asistencia.models.asistencia import Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['estado', 'permiso_solicitado', 'justificacion', 'archivo_justificacion']
        widgets = {
            'justificacion': forms.Textarea(attrs={'rows': 2}),
        }
