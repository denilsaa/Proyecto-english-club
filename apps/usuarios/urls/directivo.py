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

urlpatterns = [
    path('panel/directivo/', panel_directivo, name='panel_directivo'),
    path('panel/directivo/registrar-administrativo/', registrar_administrativo, name='registrar_administrativo'),
    path('panel/directivo/credenciales-generadas/', credenciales_generadas, name='credenciales_generadas'),  
    path('personal/', listar_personal, name='listar_personal'),
    path('personal/editar/<int:id>/', editar_personal, name='editar_personal'),
    path('personal/eliminar/<int:id>/', eliminar_personal, name='eliminar_personal'),
    path('personal/inactivos/', listar_personal_inactivo, name='listar_personal_inactivo'),
    path('personal/reactivar/<int:id>/', reactivar_personal, name='reactivar_personal'),

]
