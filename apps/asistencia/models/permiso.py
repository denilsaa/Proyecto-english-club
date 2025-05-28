from django.db import models
from apps.estudiantes.models.estudiante import Estudiante
from apps.usuarios.models.usuario import Usuario

class Permiso(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha_permiso = models.DateField()
    motivo = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    urgente = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='documentacion/permisos/', blank=True, null=True)
    revisado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.estudiante} - {self.fecha_permiso} ({self.estado})"
