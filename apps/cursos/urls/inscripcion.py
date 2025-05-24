from django.urls import path
from apps.cursos.views.inscripcion import registrar_inscripcion, listar_inscripciones, ver_estudiantes_por_curso

urlpatterns = [
    path('registrar/', registrar_inscripcion, name='registrar_inscripcion'),
    path('listar/', listar_inscripciones, name='listar_inscripciones'),
    path('curso/<int:curso_id>/estudiantes/', ver_estudiantes_por_curso, name='ver_estudiantes_por_curso'),
    
]
