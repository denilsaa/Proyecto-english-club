from django.urls import path
from apps.usuarios.views.directivo import (
    panel_directivo,
    registrar_administrativo,
    credenciales_generadas, 
    listar_personal,
    editar_personal,
    eliminar_personal,
    listar_personal_inactivo, 
    reactivar_personal, 
)
from apps.usuarios.views.dashboard import (
    dashboard_secretaria,
    dashboard_docente,
    dashboard_padre,
    dashboard_estudiante,
)

urlpatterns = [
    path('panel/directivo/', panel_directivo, name='panel_directivo'),
    path('panel/directivo/registrar-administrativo/', registrar_administrativo, name='registrar_administrativo'),
    path('panel/directivo/credenciales-generadas/', credenciales_generadas, name='credenciales_generadas'),  
    path('personal/', listar_personal, name='listar_personal'),
    path('personal/editar/<int:id>/', editar_personal, name='editar_personal'),
    path('personal/eliminar/<int:id>/', eliminar_personal, name='eliminar_personal'),
    path('personal/inactivos/', listar_personal_inactivo, name='listar_personal_inactivo'),
    path('personal/reactivar/<int:id>/', reactivar_personal, name='reactivar_personal'),

    # Dashboards para otros roles
    path('dashboard/secretaria/', dashboard_secretaria, name='dashboard_secretaria'),
    path('dashboard/docente/', dashboard_docente, name='dashboard_docente'),
    path('dashboard/padre/', dashboard_padre, name='dashboard_padre'),
    path('dashboard/estudiante/', dashboard_estudiante, name='dashboard_estudiante'),
]
