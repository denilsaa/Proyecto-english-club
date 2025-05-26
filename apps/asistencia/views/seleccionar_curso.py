from django.shortcuts import render, redirect
from apps.cursos.models.curso import Curso
from apps.usuarios.models.usuario import Usuario

def seleccionar_curso_asistencia(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    # Filtrar cursos donde el docente sea el usuario actual
    cursos = Curso.objects.filter(docente__usuario=usuario)

    if not cursos.exists():
        return render(request, 'asistencia/no_cursos.html')

    if cursos.count() == 1:
        return redirect('registrar_asistencia_curso', curso_id=cursos.first().id)

    return render(request, 'asistencia/seleccionar_curso.html', {'cursos': cursos})
