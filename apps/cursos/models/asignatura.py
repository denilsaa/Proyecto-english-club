from django.db import models
from apps.cursos.models.curso import Curso

class Asignatura(models.Model):
    nombre = models.CharField(max_length=50)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asignaturas')

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"
