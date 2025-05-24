from django.shortcuts import render, redirect
from apps.cursos.forms.inscripcion import InscripcionForm
from apps.cursos.models.inscripcion import Inscripcion
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.personal import PersonalAdministrativo
from django.contrib import messages
from datetime import date
from django.shortcuts import render, get_object_or_404
from apps.cursos.models.curso import Curso
from apps.cursos.models.inscripcion import Inscripcion
def registrar_inscripcion(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST, request.FILES)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.fecha_inscripcion = inscripcion.fecha_inscripcion or date.today()

            usuario_id = request.session.get('usuario_id')
            if usuario_id:
                try:
                    usuario = Usuario.objects.get(id=usuario_id)
                    personal = PersonalAdministrativo.objects.get(usuario=usuario)
                    inscripcion.inscrito_por = personal
                    inscripcion.save()
                    return redirect('listar_inscripciones')
                except PersonalAdministrativo.DoesNotExist:
                    messages.error(request, "Tu cuenta no está registrada como personal administrativo.")
                    return redirect('login')
            else:
                messages.error(request, "No se encontró sesión activa.")
                return redirect('login')

    else:
        form = InscripcionForm()

    return render(request, 'inscripciones/registrar_inscripcion.html', {
        'form': form,
        'titulo': 'Registrar Inscripción'
    })


def listar_inscripciones(request):
    inscripciones = Inscripcion.objects.select_related('estudiante', 'curso').order_by('-fecha_inscripcion')
    return render(request, 'inscripciones/listar_inscripciones.html', {
        'inscripciones': inscripciones,
        'titulo': 'Lista de Inscripciones'
    })

def ver_estudiantes_por_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    inscripciones = Inscripcion.objects.filter(curso=curso).select_related('estudiante')

    return render(request, 'cursos/estudiantes_por_curso.html', {
        'curso': curso,
        'inscripciones': inscripciones
    })