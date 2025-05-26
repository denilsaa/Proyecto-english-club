from django.shortcuts import render, redirect
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.personal import PersonalAdministrativo
from apps.usuarios.forms.personal import PersonalAdministrativoForm
from apps.usuarios.utils import verificar_sesion_rol
import secrets
import hashlib
from django.shortcuts import render
from apps.usuarios.models.personal import PersonalAdministrativo
from django.shortcuts import render, get_object_or_404, redirect
from apps.usuarios.forms.personal import PersonalAdministrativoForm
from apps.usuarios.models.personal import PersonalAdministrativo
from apps.cursos.models.curso import Curso
from apps.usuarios.models.usuario import Usuario
@verificar_sesion_rol('directivo')
def panel_directivo(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)

    # Filtrar cursos donde el docente sea el usuario actual
    cursos = Curso.objects.filter(docente__usuario=usuario)

    return render(request, 'paneles/directivo.html', {
        'nombre': usuario.nombre_usuario,
        'cursos': cursos,
    })


@verificar_sesion_rol('directivo')
def registrar_administrativo(request):
    if request.method == 'POST':
        form = PersonalAdministrativoForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data

            iniciales = datos['nombres'][0].lower() + datos['apellidos'].split()[0].lower()
            nombre_usuario = f"{iniciales}{datos['ci']}"
            contrasena_plana = '12345678'  # Contraseña por defecto

            if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                form.add_error(None, "Ese usuario ya existe.")
            else:
                # Generar salt y hash sin modificar el modelo
                salt = secrets.token_hex(16)
                contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()
                
                # Crear usuario con los campos existentes
                usuario = Usuario(
                    nombre_usuario=nombre_usuario,
                    contrasena=contrasena_hash,
                    correo=salt  # Usamos correo para guardar el salt temporalmente
                )
                usuario.save()
                
                PersonalAdministrativo.objects.create(usuario=usuario, **datos)
                request.session['credenciales_generadas'] = {
                    'usuario': nombre_usuario,
                    'contrasena': contrasena_plana
                }
                return redirect('credenciales_generadas')

    else:
        form = PersonalAdministrativoForm()

    return render(request, 'paneles/registrar_administrativo.html', {'form': form})

def credenciales_generadas(request):
    datos = request.session.pop('credenciales_generadas', None)
    if not datos:
        return redirect('panel_directivo')
    return render(request, 'paneles/credenciales.html', datos)


def listar_personal(request):
    personal = PersonalAdministrativo.objects.filter(activo=True).order_by('rol', 'nombres')
    return render(request, 'paneles/listar_personal.html', {'personal': personal})


def editar_personal(request, id):
    personal = get_object_or_404(PersonalAdministrativo, id=id)

    if request.method == 'POST':
        form = PersonalAdministrativoForm(request.POST, request.FILES, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('listar_personal')
    else:
        form = PersonalAdministrativoForm(instance=personal)

    return render(request, 'paneles/editar_personal.html', {
        'form': form,
        'personal': personal
    })

def eliminar_personal(request, id):
    personal = get_object_or_404(PersonalAdministrativo, id=id)
    
    if request.method == 'POST':
        personal.activo = False
        personal.save()
        return redirect('listar_personal')
    
    return render(request, 'paneles/eliminar_personal.html', {'personal': personal})

def listar_personal_inactivo(request):
    personal = PersonalAdministrativo.objects.filter(activo=False).order_by('rol', 'nombres')
    return render(request, 'paneles/listar_personal_inactivo.html', {'personal': personal})

def reactivar_personal(request, id):
    personal = get_object_or_404(PersonalAdministrativo, id=id, activo=False)
    personal.activo = True
    personal.save()
    return redirect('listar_personal_inactivo')
