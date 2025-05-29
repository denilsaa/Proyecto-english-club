from functools import wraps
from django.shortcuts import redirect

def verificar_sesion_rol(roles_permitidos):
    if isinstance(roles_permitidos, str):
        roles_permitidos = [roles_permitidos]
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'usuario_id' not in request.session:
                return redirect('login')
            rol_actual = request.session.get('rol')
            if rol_actual not in roles_permitidos:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador