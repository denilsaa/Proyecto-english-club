from django.shortcuts import render, redirect
from apps.usuarios.models.usuario import Usuario
from apps.estudiantes.models.estudiante import Estudiante
from apps.estudiantes.forms.tecnico import EstudianteTecnicoForm
from apps.usuarios.utils import verificar_sesion_rol
import hashlib
import secrets
import string
from apps.estudiantes.models.estudiante import Estudiante
from django.shortcuts import render, get_object_or_404, redirect
from apps.estudiantes.models.estudiante import Estudiante
from apps.estudiantes.forms.tecnico import EstudianteTecnicoForm

@verificar_sesion_rol('directivo')
def registrar_estudiante_tecnico(request):
    if request.method == 'POST':
        form = EstudianteTecnicoForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data

            iniciales = datos['nombres'][0].lower() + datos['apellidos'].split()[0].lower()
            nombre_usuario = f"{iniciales}{datos['ci']}"

            # Generar contraseña aleatoria
            caracteres = string.ascii_letters + string.digits
            contrasena_plana = ''.join(secrets.choice(caracteres) for _ in range(10))

            if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                form.add_error(None, "Ya existe un usuario con ese nombre.")
            else:
                salt = secrets.token_hex(8)
                contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

                usuario = Usuario.objects.create(
                    nombre_usuario=nombre_usuario,
                    contrasena=contrasena_hash,
                    correo=salt  # usando temporalmente como salt
                )

                Estudiante.objects.create(
                    usuario=usuario,
                    tipo='tecnico',
                    padre=None,
                    **datos
                )

                request.session['credenciales_generadas'] = {
                    'usuario': nombre_usuario,
                    'contrasena': contrasena_plana
                }

                return redirect('credenciales_generadas_estudiante')

    else:
        form = EstudianteTecnicoForm()

    return render(request, 'estudiantes/registrar_tecnico.html', {'form': form})


def credenciales_generadas_estudiante(request):
    datos = request.session.pop('credenciales_generadas', None)
    if not datos:
        return redirect('panel_directivo')
    return render(request, 'estudiantes/paneles/credenciales_estudiante.html', {'credenciales': datos})

def listar_tecnicos(request):
    estudiantes = Estudiante.objects.filter(tipo='tecnico', activo=True).order_by('nombres')
    return render(request, 'estudiantes/paneles/listar_tecnicos.html', {'estudiantes': estudiantes})

def editar_tecnico(request, id):
    estudiante = get_object_or_404(Estudiante, id=id, tipo='tecnico')

    if request.method == 'POST':
        form = EstudianteTecnicoForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('listar_tecnicos')
    else:
        form = EstudianteTecnicoForm(instance=estudiante)

    return render(request, 'estudiantes/paneles/editar_tecnico.html', {
        'form': form,
        'estudiante': estudiante
    })

def eliminar_tecnico(request, id):
    estudiante = get_object_or_404(Estudiante, id=id, tipo='tecnico')

    if request.method == 'POST':
        estudiante.activo = False
        estudiante.save()
        return redirect('listar_tecnicos')

    return render(request, 'estudiantes/paneles/eliminar_tecnico.html', {
        'estudiante': estudiante
    })

def listar_tecnicos_inactivos(request):
    estudiantes = Estudiante.objects.filter(tipo='tecnico', activo=False).order_by('nombres')
    return render(request, 'estudiantes/paneles/listar_tecnicos_inactivos.html', {'estudiantes': estudiantes})

def reactivar_tecnico(request, id):
    estudiante = get_object_or_404(Estudiante, id=id, tipo='tecnico', activo=False)
    estudiante.activo = True
    estudiante.save()
    return redirect('listar_tecnicos_inactivos')
