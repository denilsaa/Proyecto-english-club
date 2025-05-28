from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from apps.asistencia.models.permiso import Permiso
from apps.estudiantes.models.estudiante import Estudiante
from django.contrib.auth.decorators import login_required

@login_required
def solicitar_permiso(request):
    # Verificar que el usuario tenga un perfil de estudiante asociado
    estudiante = getattr(request.user, 'estudiante', None)
    if not estudiante:
        messages.error(request, "Solo los estudiantes pueden solicitar permisos.")
        return redirect('home')  

    if request.method == 'POST':
        fecha_permiso = request.POST.get('fecha_permiso')
        motivo = request.POST.get('motivo')
        urgente = bool(request.POST.get('urgente'))
        archivo = request.FILES.get('archivo')

        # Crear el permiso
        Permiso.objects.create(
            estudiante=estudiante,
            fecha_permiso=fecha_permiso,
            motivo=motivo,
            urgente=urgente,
            archivo=archivo,
        )

        messages.success(request, "Permiso solicitado correctamente.")
        return redirect('home')

    return render(request, 'asistencia/solicitar_permiso.html')
