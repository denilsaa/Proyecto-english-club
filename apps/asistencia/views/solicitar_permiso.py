from apps.asistencia.utils import verificar_sesion_rol
from apps.asistencia.forms.permiso_forms import PermisoForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from apps.usuarios.utils import verificar_sesion_rol
from apps.asistencia.models.permiso import Permiso
@verificar_sesion_rol(['estudiante'])
def solicitar_permiso(request):
    usuario = getattr(request, 'usuario_actual', None)
    estudiante = getattr(usuario, 'estudiante', None)
    if not estudiante:
        messages.error(request, "Solo los estudiantes pueden solicitar permisos.")
        return redirect('login')

    if request.method == 'POST':
        form = PermisoForm(request.POST, request.FILES)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.estudiante = estudiante
            permiso.estado = 'pendiente'
            permiso.creado_por = usuario
            permiso.save()
            messages.success(request, "Permiso solicitado correctamente.")
            return redirect('dashboard_estudiante')  # Ajusta según tu URL
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = PermisoForm()

    return render(request, 'asistencia/solicitar_permiso.html', {'form': form})

@verificar_sesion_rol(['directivo', 'secretaria'])
def lista_permisos_pendientes(request):
    permisos = Permiso.objects.filter(estado='pendiente').order_by('fecha_inicio')
    return render(request, 'asistencia/lista_permisos_pendientes.html', {'permisos': permisos})