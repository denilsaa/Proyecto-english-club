from django.urls import path
from apps.estudiantes.views.regular import (
    registrar_estudiante_regular,
    credenciales_generadas_estudiante_regular,
    listar_regulares,
    editar_estudiante_regular,
    eliminar_estudiante_regular,
    listar_regulares_inactivos,
    reactivar_estudiante_regular,
)

urlpatterns = [
    path('panel/directivo/registrar-estudiante-regular/', registrar_estudiante_regular, name='registrar_estudiante_regular'),
    path('panel/directivo/credenciales-estudiante-regular/', credenciales_generadas_estudiante_regular, name='credenciales_generadas_estudiante_regular'),
    path('panel/directivo/estudiante-regular/editar/<int:id>/', editar_estudiante_regular, name='editar_estudiante_regular'),
    path('panel/directivo/estudiante-regular/eliminar/<int:id>/', eliminar_estudiante_regular, name='eliminar_estudiante_regular'), 
    path('panel/directivo/estudiantes-regulares/', listar_regulares, name='listar_regulares'),
    path('panel/directivo/estudiantes-regulares-inactivos/', listar_regulares_inactivos, name='listar_regulares_inactivos'),
    path('panel/directivo/estudiante-regular/reactivar/<int:id>/', reactivar_estudiante_regular, name='reactivar_estudiante_regular'),    
]
