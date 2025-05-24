from django import forms
from apps.estudiantes.models.estudiante import Estudiante
from apps.usuarios.models.padre import Padre

class EstudianteRegularForm(forms.ModelForm):
    padre_nombres = forms.CharField(max_length=100)
    padre_apellidos = forms.CharField(max_length=100)
    padre_ci = forms.CharField(max_length=20)
    padre_direccion = forms.CharField(max_length=200)
    padre_telefono = forms.CharField(max_length=20)
    padre_fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Estudiante
        exclude = ['usuario', 'tipo', 'ocupacion', 'padre']
