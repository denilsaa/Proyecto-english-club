from django.db import models
from apps.usuarios.models.personal import PersonalAdministrativo

class Publicacion(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(PersonalAdministrativo, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
