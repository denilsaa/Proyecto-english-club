from django.urls import path
from apps.asistencia.views.seleccionar_curso import seleccionar_curso_asistencia
from apps.asistencia.views.registrar_asistencia import registrar_asistencia_curso
from apps.asistencia.views.listar_asistencia import listar_asistencias_curso
from apps.asistencia.views.solicitar_permiso import solicitar_permiso
from apps.asistencia.views.solicitar_permiso import lista_permisos_pendientes

urlpatterns = [
    path('seleccionar/', seleccionar_curso_asistencia, name='seleccionar_curso_asistencia'),
    path('curso/<int:curso_id>/asistencia/', registrar_asistencia_curso, name='registrar_asistencia_curso'),
    path('curso/<int:curso_id>/asistencia/listar/', listar_asistencias_curso, name='listar_asistencias_curso'),
    path('solicitar-permiso/', solicitar_permiso, name='solicitar_permiso'),
    path('permisos/pendientes/', lista_permisos_pendientes, name='lista_permisos_pendientes'),
    

]
