from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.cursos.models.curso import Curso
from apps.cursos.models.asignatura import Asignatura

@receiver(post_save, sender=Curso)
def crear_asignaturas_defecto(sender, instance, created, **kwargs):
    if created and instance.asignaturas.count() == 0:
        asignaturas = [
            'Grammar', 'Reading', 'Listening',
            'Writing', 'Speaking', 'Responsibility', 'Class Development'
        ]
        for nombre in asignaturas:
            Asignatura.objects.create(nombre=nombre, curso=instance)
