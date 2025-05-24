import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.usuarios.models import Usuario, PersonalAdministrativo
import hashlib
import secrets

def crear_usuario_directivo():
    if not Usuario.objects.filter(nombre_usuario='dadmin').exists():
        contrasena_plana = 'admin123'
        salt = secrets.token_hex(8)
        contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

        usuario = Usuario.objects.create(
            nombre_usuario='dadmin',
            contrasena=contrasena_hash,
            correo=salt
        )

        PersonalAdministrativo.objects.create(
            usuario=usuario,
            rol='directivo',
            nombres='Admin',
            apellidos='Principal',
            ci='12345678',
            direccion='Av. Siempre Viva 123',
            telefono='70000000',
            fecha_nacimiento='1990-01-01'
        )

        print(f"✅ Usuario 'dadmin' creado con contraseña: {contrasena_plana}")
    else:
        print("⚠️ El usuario 'dadmin' ya existe.")

if __name__ == '__main__':
    crear_usuario_directivo()
