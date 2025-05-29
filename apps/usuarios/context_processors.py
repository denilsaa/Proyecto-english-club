from apps.asistencia.models.permiso import Permiso

def notificaciones_context(request):
    if not request.session.get('usuario_id'):
        return {}

    rol = request.session.get('rol')
    notificaciones = []

    if rol in ['directivo', 'secretaria']:
        pendientes = Permiso.objects.filter(estado='pendiente').count()
        if pendientes > 0:
            notificaciones.append({
                'tipo': 'permiso_pendiente',
                'mensaje': f'Tienes {pendientes} permiso(s) pendiente(s) por revisar.',
                'url': '/asistencia/permisos/pendientes/',  # ✅ URL correcta
            })

    return {'notificaciones': notificaciones}
