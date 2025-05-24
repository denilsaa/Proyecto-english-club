from django.db import models
from .usuario import Usuario

class PersonalAdministrativo(models.Model):
    ROLES = [
        ("directivo", "Directivo"),
        ("docente", "Docente"),
        ("secretaria", "Secretaria"),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ci = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    archivo_documentacion = models.FileField(upload_to="documentacion/personal/", blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.rol})"
