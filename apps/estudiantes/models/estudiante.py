from django.db import models
from apps.usuarios.models.padre import Padre

class Estudiante(models.Model):
    TIPOS = [
        ('regular', 'Regular'),
        ('tecnico', 'Técnico'),
    ]

    GRUPOS = [
        ('Sweet', 'Sweet'),
        ('Smart', 'Smart'),
        ('Teens', 'Teens'),
    ]
    usuario = models.OneToOneField('usuarios.Usuario', on_delete=models.CASCADE, null=True, blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    ci = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    grupo = models.CharField(max_length=20, choices=GRUPOS, blank=True, null=True)
    colegio_universidad = models.CharField(max_length=100)
    ocupacion = models.CharField(max_length=100)
    padre = models.ForeignKey(Padre, on_delete=models.SET_NULL, null=True, blank=True)
    archivo_documentacion = models.FileField(upload_to='documentacion/estudiantes/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.tipo})"
