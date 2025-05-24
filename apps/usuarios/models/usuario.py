# apps/usuarios/models/usuario.py
from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)
    correo = models.EmailField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_usuario
