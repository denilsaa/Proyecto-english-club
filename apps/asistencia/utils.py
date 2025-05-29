from django.shortcuts import redirect
from functools import wraps
from apps.usuarios.models.usuario import Usuario

def verificar_sesion_rol(roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return redirect('login')
            
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                return redirect('login')

            # Guardar usuario en request para uso en la vista
            request.usuario_actual = usuario

            # Validar rol
            rol_actual = request.session.get('rol')
            if rol_actual not in roles_permitidos:
                # Opcional: mostrar mensaje o redirigir a página de no autorizado
                return redirect('login')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
