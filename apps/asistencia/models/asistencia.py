from django.db import models
from apps.estudiantes.models.estudiante import Estudiante
from apps.cursos.models.curso import Curso
from apps.usuarios.models.usuario import Usuario

class Asistencia(models.Model):
    ESTADOS = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('justificado', 'Justificado'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    permiso_solicitado = models.BooleanField(default=False)
    archivo_justificacion = models.FileField(upload_to='documentacion/asistencias/', blank=True, null=True)
    justificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.estudiante} - {self.estado}"
