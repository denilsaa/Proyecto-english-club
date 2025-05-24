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
    path('panel/directivo/registrar-estudiante-tecnico/', registrar_estudiante_tecnico, name='registrar_estudiante_tecnico'),
    path('panel/directivo/credenciales-estudiante/', credenciales_generadas_estudiante, name='credenciales_generadas_estudiante'),
    path('listar/', listar_tecnicos, name='listar_tecnicos'),
    path('editar/<int:id>/', editar_tecnico, name='editar_tecnico'),
    path('eliminar/<int:id>/', eliminar_tecnico, name='eliminar_tecnico'),
    path('inactivos/', listar_tecnicos_inactivos, name='listar_tecnicos_inactivos'),
    path('reactivar/<int:id>/', reactivar_tecnico, name='reactivar_tecnico'),    
]
