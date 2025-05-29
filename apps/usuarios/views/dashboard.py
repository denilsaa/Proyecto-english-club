from django.shortcuts import render
from apps.usuarios.utils import verificar_sesion_rol

@verificar_sesion_rol('directivo')
def panel_directivo(request):
    # Datos para directivo
    return render(request, 'paneles/directivo.html', {})

@verificar_sesion_rol('secretaria')
def dashboard_secretaria(request):
    return render(request, 'paneles/secretaria.html')

@verificar_sesion_rol('docente')
def dashboard_docente(request):
    # Datos para docente
    return render(request, 'paneles/docente.html', {})

@verificar_sesion_rol('padre')
def dashboard_padre(request):
    # Datos para padre
    return render(request, 'paneles/padre.html', {})

@verificar_sesion_rol('estudiante')
def dashboard_estudiante(request):
    # Datos para estudiante
    return render(request, 'paneles/estudiante.html', {})
