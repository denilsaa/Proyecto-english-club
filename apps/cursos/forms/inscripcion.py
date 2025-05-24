from django import forms
from apps.cursos.models.inscripcion import Inscripcion
from apps.cursos.models.curso import Curso
from apps.estudiantes.models.estudiante import Estudiante

class InscripcionForm(forms.ModelForm):
    mostrar_todos = forms.BooleanField(
        required=False,
        label="Permitir inscribir estudiante de otro tipo",
        help_text="Marcar si deseas incluir estudiantes de otro tipo de curso.",
    )

    class Meta:
        model = Inscripcion
        fields = ['curso', 'estudiante', 'fecha_inscripcion', 'modalidad', 'medio_referencia', 'motivo', 'archivo_formulario']
        widgets = {
            'fecha_inscripcion': forms.DateInput(attrs={'type': 'date'}),
            'modalidad': forms.TextInput(attrs={'class': 'input'}),
            'medio_referencia': forms.TextInput(attrs={'class': 'input'}),
            'motivo': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay datos cargados (POST o instancia con curso ya asignado)
        curso = None
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                curso = Curso.objects.get(id=curso_id)
            except (ValueError, Curso.DoesNotExist):
                pass
        elif self.instance and self.instance.pk:
            curso = self.instance.curso

        # Filtro de estudiantes según tipo de curso
        if curso and not self.data.get('mostrar_todos'):
            self.fields['estudiante'].queryset = Estudiante.objects.filter(tipo=curso.tipo_estudiante)
        else:
            self.fields['estudiante'].queryset = Estudiante.objects.all()


def clean(self):
    cleaned_data = super().clean()
    estudiante = cleaned_data.get('estudiante')
    
    if estudiante:
        # Verifica si ya está inscrito en otro curso
        existe = Inscripcion.objects.filter(estudiante=estudiante)
        if self.instance.pk:
            # Si está editando, no contar la inscripción actual
            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():
            raise forms.ValidationError("Este estudiante ya está inscrito en un curso.")
    
    return cleaned_data