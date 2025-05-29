from django.shortcuts import render
from apps.usuarios.utils import verificar_sesion_rol
from apps.asistencia.models.permiso import Permiso
from apps.cursos.models import Curso

@verificar_sesion_rol(['directivo'])
def dashboard_directivo(request):
    permisos_pendientes = Permiso.objects.filter(estado='pendiente').count()
    cursos = Curso.objects.all()  # o filtra según necesidad
    return render(request, 'directivo/dashboard.html', {
        'permisos_pendientes': permisos_pendientes,
        'cursos': cursos,
    })

@verificar_sesion_rol(['secretaria'])
def dashboard_secretaria(request):
    return render(request, 'paneles/secretaria.html')

@verificar_sesion_rol(['docente'])
def dashboard_docente(request):
    # Datos para docente
    return render(request, 'paneles/docente.html', {})

@verificar_sesion_rol(['padre'])
def dashboard_padre(request):
    # Datos para padre
    return render(request, 'paneles/padre.html', {})

@verificar_sesion_rol(['estudiante'])
def dashboard_estudiante(request):
    # Datos para estudiante
    return render(request, 'paneles/estudiante.html', {})
