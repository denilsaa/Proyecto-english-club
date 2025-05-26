from django.urls import path
from apps.asistencia.views.seleccionar_curso import seleccionar_curso_asistencia
from apps.asistencia.views.registrar_asistencia import registrar_asistencia_curso
from apps.asistencia.views.listar_asistencia import listar_asistencias_curso

urlpatterns = [
    path('seleccionar/', seleccionar_curso_asistencia, name='seleccionar_curso_asistencia'),
    path('curso/<int:curso_id>/asistencia/', registrar_asistencia_curso, name='registrar_asistencia_curso'),
    path('curso/<int:curso_id>/asistencia/listar/', listar_asistencias_curso, name='listar_asistencias_curso'),
]
