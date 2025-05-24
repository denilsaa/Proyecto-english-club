from django import forms
from apps.cursos.models.curso import Curso
from apps.usuarios.models.personal import PersonalAdministrativo

DIAS_SEMANA = [
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miércoles', 'Miércoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sábado', 'Sábado'),
]

class CursoForm(forms.ModelForm):
    dias = forms.MultipleChoiceField(
        choices=DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
        required=True
    )

    class Meta:
        model = Curso
        fields = ['nombre', 'docente', 'gestion', 'dias', 'hora_inicio', 'hora_fin', 'tipo_estudiante']  # ← AGREGADO
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input'}),
            'docente': forms.Select(attrs={'class': 'input'}),
            'gestion': forms.TextInput(attrs={'class': 'input'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
            'tipo_estudiante': forms.Select(attrs={'class': 'input'}),  # ← OPCIONAL para estética
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['docente'].queryset = PersonalAdministrativo.objects.filter(rol__in=['docente', 'directivo'])

        if self.instance and self.instance.pk and self.instance.dias:
            self.fields['dias'].initial = self.instance.dias.split(', ')

    def clean_dias(self):
        dias = self.cleaned_data['dias']
        if len(dias) > 6:
            raise forms.ValidationError("Solo puedes seleccionar hasta 6 días.")
        return dias

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.dias = ', '.join(self.cleaned_data['dias'])
        if commit:
            instance.save()
        return instance
