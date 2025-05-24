from django.db import models
from apps.estudiantes.models.estudiante import Estudiante
from apps.cursos.models.curso import Curso
from apps.usuarios.models.usuario import Usuario
from apps.cursos.models.asignatura import Asignatura

class Nota(models.Model):
    TIPOS_EVALUACION = [
        ('participacion', 'Participación'),
        ('oral', 'Oral'),
        ('tarea', 'Tarea'),
        ('mensual', 'Mensual'),
        ('final', 'Final'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo_evaluacion = models.CharField(max_length=50, choices=TIPOS_EVALUACION)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    observacion = models.CharField(max_length=255)
    gestion = models.CharField(max_length=10)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.estudiante} - {self.tipo_evaluacion}: {self.nota}"
