# apps/asistencia/forms/permiso_forms.py

from django import forms
from apps.asistencia.models.permiso import Permiso

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['fecha_inicio', 'fecha_fin', 'motivo', 'urgente', 'archivo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }
