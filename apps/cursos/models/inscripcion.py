from django.db import models
from apps.estudiantes.models.estudiante import Estudiante
from apps.cursos.models.curso import Curso
from apps.usuarios.models.personal import PersonalAdministrativo

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField()
    modalidad = models.CharField(max_length=50)
    medio_referencia = models.CharField(max_length=50)
    motivo = models.CharField(max_length=200)
    archivo_formulario = models.FileField(upload_to="documentacion/inscripciones/", blank=True, null=True)
    inscrito_por = models.ForeignKey(PersonalAdministrativo, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} → {self.curso}"
