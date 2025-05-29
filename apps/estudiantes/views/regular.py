from django.shortcuts import render, redirect, get_object_or_404
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.padre import Padre
from apps.estudiantes.models.estudiante import Estudiante
from apps.estudiantes.forms.regular import EstudianteRegularForm
from apps.usuarios.utils import verificar_sesion_rol
import hashlib, secrets, string

@verificar_sesion_rol(['directivo', 'secretaria'])
def registrar_estudiante_regular(request):
    if request.method == 'POST':
        form = EstudianteRegularForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data

            # Generar nombre de usuario del padre
            iniciales = datos['padre_nombres'][0].lower() + datos['padre_apellidos'].split()[0].lower()
            nombre_usuario = f"{iniciales}{datos['padre_ci']}"

            if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                form.add_error(None, "Ya existe un usuario con ese nombre.")
            else:
                # Generar contraseña aleatoria segura
                caracteres = string.ascii_letters + string.digits
                contrasena_plana = ''.join(secrets.choice(caracteres) for _ in range(10))
                salt = secrets.token_hex(8)
                contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

                # Crear usuario del padre
                usuario_padre = Usuario.objects.create(
                    nombre_usuario=nombre_usuario,
                    contrasena=contrasena_hash,
                    correo=salt  # temporal, se usa como salt
                )

                # Crear registro de padre
                padre = Padre.objects.create(
                    usuario=usuario_padre,
                    nombres=datos['padre_nombres'],
                    apellidos=datos['padre_apellidos'],
                    ci=datos['padre_ci'],
                    direccion=datos['padre_direccion'],
                    telefono=datos['padre_telefono'],
                    fecha_nacimiento=datos['padre_fecha_nacimiento']
                )

                # Crear estudiante regular
                Estudiante.objects.create(
                    nombres=datos['nombres'],
                    apellidos=datos['apellidos'],
                    fecha_nacimiento=datos['fecha_nacimiento'],
                    ci=datos['ci'],
                    direccion=datos['direccion'],
                    telefono=datos['telefono'],
                    tipo='regular',
                    grupo=datos['grupo'],
                    colegio_universidad=datos['colegio_universidad'],
                    archivo_documentacion=datos['archivo_documentacion'],
                    padre=padre,
                    usuario=None  # El estudiante regular no tiene acceso directo
                )

                # Guardar credenciales en sesión para mostrar después
                request.session['credenciales_generadas'] = {
                    'usuario': nombre_usuario,
                    'contrasena': contrasena_plana
                }

                return redirect('credenciales_generadas_estudiante_regular')
    else:
        form = EstudianteRegularForm()

    return render(request, 'estudiantes/registrar_regular.html', {'form': form})

@verificar_sesion_rol(['directivo', 'secretaria'])
def credenciales_generadas_estudiante_regular(request):
    credenciales = request.session.pop('credenciales_generadas', None)
    if not credenciales:
        return redirect('panel_directivo')  # O a un dashboard común si quieres
    return render(request, 'estudiantes/paneles/credenciales_estudiante_regular.html', {'credenciales': credenciales})

@verificar_sesion_rol(['directivo', 'secretaria'])
def listar_regulares(request):
    estudiantes = Estudiante.objects.filter(tipo='regular', activo=True).select_related('padre').order_by('nombres')
    return render(request, 'estudiantes/paneles/listar_regulares.html', {'estudiantes': estudiantes})

@verificar_sesion_rol(['directivo', 'secretaria'])
def editar_estudiante_regular(request, id):
    estudiante = get_object_or_404(Estudiante, id=id, tipo='regular')
    padre = estudiante.padre

    if request.method == 'POST':
        form = EstudianteRegularForm(request.POST, request.FILES, instance=estudiante)

        if form.is_valid():
            estudiante = form.save(commit=False)
            estudiante.tipo = 'regular'
            estudiante.save()

            padre.nombres = form.cleaned_data['padre_nombres']
            padre.apellidos = form.cleaned_data['padre_apellidos']
            padre.ci = form.cleaned_data['padre_ci']
            padre.direccion = form.cleaned_data['padre_direccion']
            padre.telefono = form.cleaned_data['padre_telefono']
            padre.fecha_nacimiento = form.cleaned_data['padre_fecha_nacimiento']
            padre.save()

            return redirect('listar_regulares')
    else:
        initial_data = {
            'padre_nombres': padre.nombres,
            'padre_apellidos': padre.apellidos,
            'padre_ci': padre.ci,
            'padre_direccion': padre.direccion,
            'padre_telefono': padre.telefono,
            'padre_fecha_nacimiento': padre.fecha_nacimiento,
        }
        form = EstudianteRegularForm(instance=estudiante, initial=initial_data)

    return render(request, 'estudiantes/paneles/editar_regular.html', {
        'form': form,
        'estudiante': estudiante
    })

@verificar_sesion_rol(['directivo', 'secretaria'])
def eliminar_estudiante_regular(request, id):
    estudiante = get_object_or_404(Estudiante, id=id, tipo='regular', activo=True)

    if request.method == 'POST':
        estudiante.activo = False
        estudiante.save()
        return redirect('listar_regulares')

    return render(request, 'estudiantes/paneles/eliminar_regular.html', {
        'estudiante': estudiante
    })

@verificar_sesion_rol(['directivo', 'secretaria'])
def listar_regulares_inactivos(request):
    estudiantes = Estudiante.objects.filter(tipo='regular', activo=False).select_related('padre').order_by('nombres')
    return render(request, 'estudiantes/paneles/listar_regulares_inactivos.html', {
        'estudiantes': estudiantes
    })

@verificar_sesion_rol(['directivo', 'secretaria'])
def reactivar_estudiante_regular(request, id):
    estudiante = get_object_or_404(Estudiante, id=id, tipo='regular', activo=False)
    estudiante.activo = True
    estudiante.save()
    return redirect('listar_regulares_inactivos')
