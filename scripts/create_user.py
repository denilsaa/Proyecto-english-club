import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.usuarios.models import Usuario, PersonalAdministrativo
from apps.estudiantes.models.estudiante import Estudiante
import hashlib
import secrets
from datetime import date


def crear_usuario(nombre_usuario, rol, nombres, apellidos, ci, direccion, telefono, fecha_nacimiento):
    if not Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
        contrasena_plana = 'admin123'
        salt = secrets.token_hex(8)
        contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

        usuario = Usuario.objects.create(
            nombre_usuario=nombre_usuario,
            contrasena=contrasena_hash,
            correo=salt  # Usas correo para guardar el salt temporalmente
        )

        PersonalAdministrativo.objects.create(
            usuario=usuario,
            rol=rol,
            nombres=nombres,
            apellidos=apellidos,
            ci=ci,
            direccion=direccion,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento
        )

        print(f"✅ Usuario '{nombre_usuario}' creado con rol '{rol}' y contraseña: {contrasena_plana}")
    else:
        print(f"⚠️ El usuario '{nombre_usuario}' ya existe.")


def crear_estudiante(nombre_usuario, nombres, apellidos, ci, fecha_nacimiento, tipo_estudiante):
    # Crea Usuario y Estudiante técnico o regular según tipo_estudiante
    if not Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
        contrasena_plana = 'admin123'
        salt = secrets.token_hex(8)
        contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

        usuario = Usuario.objects.create(
            nombre_usuario=nombre_usuario,
            contrasena=contrasena_hash,
            correo=salt
        )

        estudiante = Estudiante.objects.create(
            usuario=usuario,
            nombres=nombres,
            apellidos=apellidos,
            ci=ci,
            fecha_nacimiento=fecha_nacimiento,
            tipo=tipo_estudiante  # Asumiendo campo tipo: 'tecnico' o 'regular'
        )

        print(f"✅ Estudiante '{nombre_usuario}' creado como '{tipo_estudiante}' con contraseña: {contrasena_plana}")
    else:
        print(f"⚠️ El usuario '{nombre_usuario}' ya existe.")


if __name__ == '__main__':
    crear_usuario('dadmin', 'directivo', 'Admin', 'Principal', '12345678', 'Av. Siempre Viva 123', '70000000', date(1990, 1, 1))
    crear_usuario('secretaria1', 'secretaria', 'Ana', 'Lopez', '87654321', 'Calle Falsa 456', '70123456', date(1992, 5, 10))
    crear_usuario('docente1', 'docente', 'Carlos', 'Martinez', '11223344', 'Av. Central 789', '70234567', date(1985, 7, 20))
    crear_usuario('padre1', 'padre', 'Jorge', 'Perez', '55667788', 'Calle Luna 123', '70345678', date(1975, 3, 15))
    crear_estudiante('estudiante_tecnico1', 'Luis', 'Gomez', '99887766', date(2005, 9, 5), 'tecnico')
    crear_estudiante('estudiante_regular1', 'Maria', 'Fernandez', '88776655', date(2008, 12, 20), 'regular')
