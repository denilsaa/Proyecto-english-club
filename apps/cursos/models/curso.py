from django.db import models
from apps.usuarios.models.personal import PersonalAdministrativo

class Curso(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
    ]

    TIPOS_ESTUDIANTE = [
        ('tecnico', 'Técnico'),
        ('regular', 'Regular'),
    ]

    nombre = models.CharField(max_length=100)
    docente = models.ForeignKey(PersonalAdministrativo, on_delete=models.CASCADE)
    gestion = models.CharField(max_length=10)
    dias = models.CharField(max_length=150)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo_estudiante = models.CharField(max_length=10, choices=TIPOS_ESTUDIANTE, default='regular')  # ← NUEVO
    activo = models.BooleanField(default=True)  # ← NUEVO

    def __str__(self):
        return self.nombre

    def dias_list(self):
        if self.dias:
            return [d.strip() for d in self.dias.split(',')]
        return []
