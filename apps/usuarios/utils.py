from django.shortcuts import redirect
from functools import wraps

def verificar_sesion_rol(rol_permitido):
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'usuario_id' not in request.session:
                return redirect('login')
            if request.session.get('rol') != rol_permitido:
                return redirect('login')  # O mostrar error 403 personalizado
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador
