from django.db import models
from apps.estudiantes.models.estudiante import Estudiante
from apps.usuarios.models.padre import Padre
from apps.usuarios.models.personal import PersonalAdministrativo

class ResultadoVARK(models.Model):
    ORIGENES = [
        ('padre', 'Padre'),
        ('directivo', 'Directivo'),
        ('estudiante_tecnico', 'Estudiante Técnico'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo_dominante = models.CharField(max_length=20)
    gestion = models.CharField(max_length=10)
    origen = models.CharField(max_length=20, choices=ORIGENES)
    resultado_sql_id = models.CharField(max_length=50)
    registrado_por_padre = models.ForeignKey(Padre, on_delete=models.SET_NULL, null=True, blank=True)
    registrado_por_personal = models.ForeignKey(PersonalAdministrativo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.estudiante} - {self.tipo_dominante}"
