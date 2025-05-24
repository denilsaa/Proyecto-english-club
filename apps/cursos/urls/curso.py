from django.urls import path
from apps.cursos.views import curso as curso_views

urlpatterns = [
    path('', curso_views.listar_cursos, name='listar_cursos'),
    path('crear/', curso_views.crear_curso, name='crear_curso'),
    path('editar/<int:pk>/', curso_views.editar_curso, name='editar_curso'),
    path('eliminar/<int:pk>/', curso_views.eliminar_curso, name='eliminar_curso'),
    
]
