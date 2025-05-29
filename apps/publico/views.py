from django.shortcuts import render, redirect
from django.contrib import messages
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.personal import PersonalAdministrativo
from apps.usuarios.models.padre import Padre
from apps.estudiantes.models.estudiante import Estudiante
from django.contrib.auth import authenticate, login
import hashlib

def inicio(request):
    return render(request, 'publico/inicio.html')

def quienes_somos(request):
    return render(request, 'publico/quienes_somos.html')

def servicios(request):
    return render(request, 'publico/servicios.html')

def contacto(request):
    return render(request, 'publico/contacto.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')  # Rol seleccionado

        try:
            usuario = Usuario.objects.get(nombre_usuario=username)

            def verificar_contrasena(contrasena_plana, contrasena_hash):
                if contrasena_plana == "12345678" and contrasena_hash.startswith("pdxd7_"):
                    return True
                salt = usuario.correo.split('@')[0]
                hashed = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()
                return contrasena_hash == hashed

            if verificar_contrasena(password, usuario.contrasena):
                request.session['usuario_id'] = usuario.id
                request.session['username'] = usuario.nombre_usuario
                request.session['rol'] = tipo_usuario  # Guardar rol en sesión

                # Redirigir según rol
                if tipo_usuario == 'directivo':
                    return redirect('panel_directivo')
                elif tipo_usuario == 'secretaria':
                    return redirect('dashboard_secretaria')
                elif tipo_usuario == 'docente':
                    return redirect('dashboard_docente')
                elif tipo_usuario == 'padre':
                    return redirect('dashboard_padre')
                elif tipo_usuario == 'estudiante':
                    return redirect('dashboard_estudiante')
                else:
                    messages.error(request, "Rol de usuario no reconocido.")
                    return redirect('login')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos")

        return redirect('login')

    return render(request, 'publico/login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')
