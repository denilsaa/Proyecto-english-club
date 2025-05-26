from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime
import calendar

from apps.cursos.models.curso import Curso
from apps.asistencia.models.asistencia import Asistencia

def listar_asistencias_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    fecha_str = request.GET.get('fecha')

    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha = timezone.now().date()
    else:
        fecha = timezone.now().date()

    dia_semana_nombre = calendar.day_name[fecha.weekday()]
    dia_mapeado = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    dias_curso = curso.dias_list()

    if dia_mapeado[dia_semana_nombre] not in dias_curso:
        mensaje_error = (
            f"El curso solo se imparte los días {', '.join(dias_curso)}. "
            f"La fecha seleccionada es {dia_mapeado[dia_semana_nombre]}."
        )
        asistencias = []
    else:
        mensaje_error = None
        asistencias = Asistencia.objects.filter(curso=curso, fecha=fecha).select_related('estudiante')

    return render(request, 'asistencia/listar_asistencia.html', {
        'curso': curso,
        'asistencias': asistencias,
        'fecha': fecha,
        'mensaje_error': mensaje_error
    })
