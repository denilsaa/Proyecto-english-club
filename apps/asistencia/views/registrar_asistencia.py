from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
import calendar

from apps.cursos.models.curso import Curso
from apps.estudiantes.models.estudiante import Estudiante
from apps.asistencia.models.asistencia import Asistencia

def registrar_asistencia_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    estudiantes = Estudiante.objects.filter(inscripcion__curso=curso)

    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                fecha = timezone.now().date()
        else:
            fecha = timezone.now().date()

        # Obtener día de la semana en español
        dia_semana_nombre = calendar.day_name[fecha.weekday()]  # 'Monday', 'Tuesday', ...
        dia_mapeado = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }

        # Obtener lista de días del curso
        dias_curso = curso.dias_list()

        # Validar que la fecha esté dentro de los días del curso
        if dia_mapeado[dia_semana_nombre] not in dias_curso:
            mensaje_error = (
                f"El curso solo se imparte los días {', '.join(dias_curso)}. "
                f"La fecha seleccionada es {dia_mapeado[dia_semana_nombre]}."
            )
            return render(request, 'asistencia/registrar_asistencia.html', {
                'curso': curso,
                'estudiantes': estudiantes,
                'fecha_hoy': timezone.now().date(),
                'mensaje_error': mensaje_error
            })

        # Registrar asistencias
        for estudiante in estudiantes:
            estado = request.POST.get(f"estado_{estudiante.id}")
            permiso = request.POST.get(f"permiso_{estudiante.id}") == 'true'
            justificacion = request.POST.get(f"justificacion_{estudiante.id}", '').strip()
            Asistencia.objects.create(
                estudiante=estudiante,
                curso=curso,
                fecha=fecha,
                estado=estado,
                permiso_solicitado=permiso,
                justificacion=justificacion
            )
        return redirect('listar_asistencias_curso', curso_id=curso.id)

    return render(request, 'asistencia/registrar_asistencia.html', {
        'curso': curso,
        'estudiantes': estudiantes,
        'fecha_hoy': timezone.now().date()
    })
