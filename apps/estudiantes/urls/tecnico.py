from django.urls import path
from apps.estudiantes.views.tecnico import (
    registrar_estudiante_tecnico,
    credenciales_generadas_estudiante,
    listar_tecnicos,
    editar_tecnico,
    eliminar_tecnico,
    listar_tecnicos_inactivos,
    reactivar_tecnico,
)

urlpatterns = [
    path('panel/estudiantes/registrar-tecnico/', registrar_estudiante_tecnico, name='registrar_estudiante_tecnico'),
    path('panel/estudiantes/credenciales/', credenciales_generadas_estudiante, name='credenciales_generadas_estudiante'),
    path('panel/estudiantes/listar/', listar_tecnicos, name='listar_tecnicos'),
    path('panel/estudiantes/editar/<int:id>/', editar_tecnico, name='editar_tecnico'),
    path('panel/estudiantes/eliminar/<int:id>/', eliminar_tecnico, name='eliminar_tecnico'),
    path('panel/estudiantes/inactivos/', listar_tecnicos_inactivos, name='listar_tecnicos_inactivos'),
    path('panel/estudiantes/reactivar/<int:id>/', reactivar_tecnico, name='reactivar_tecnico'),
]
