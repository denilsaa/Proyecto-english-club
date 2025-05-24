import os
import sys
import django
import hashlib
import secrets
import random
from datetime import date
from faker import Faker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.usuarios.models import Usuario, PersonalAdministrativo, Padre
from apps.estudiantes.models import Estudiante

fake = Faker("es_ES")

# Función para generar contraseña encriptada
def crear_usuario(nombre_usuario, contrasena_plana):
    salt = secrets.token_hex(8)
    contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()
    return Usuario.objects.create(
        nombre_usuario=nombre_usuario,
        contrasena=contrasena_hash,
        correo=salt  # Usas salt en el campo correo como en tu ejemplo
    )

# Crear Personal Administrativo
def crear_personal_admin(cantidad, rol):
    for _ in range(cantidad):
        nombres = fake.first_name()
        apellidos = fake.last_name()
        ci = fake.unique.random_number(digits=7)
        direccion = fake.address()
        telefono = fake.phone_number()
        fecha_nacimiento = fake.date_of_birth(minimum_age=28, maximum_age=55)
        nombre_usuario = f"{nombres.lower()}.{apellidos.lower()}.{rol}"
        usuario = crear_usuario(nombre_usuario, "12345678")

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
        print(f"✅ {rol.capitalize()} creado: {nombre_usuario}")

# Crear Estudiantes Técnicos
def crear_estudiantes_tecnicos(cantidad):
    for _ in range(cantidad):
        nombres = fake.first_name()
        apellidos = fake.last_name()
        ci = fake.unique.random_number(digits=7)
        direccion = fake.address()
        telefono = fake.phone_number()
        fecha_nacimiento = fake.date_of_birth(minimum_age=16, maximum_age=30)
        colegio_universidad = fake.company()
        ocupacion = fake.job()
        nombre_usuario = f"{nombres.lower()}.{apellidos.lower()}.tec"
        usuario = crear_usuario(nombre_usuario, "12345678")

        Estudiante.objects.create(
            usuario=usuario,
            nombres=nombres,
            apellidos=apellidos,
            ci=ci,
            direccion=direccion,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            tipo="tecnico",
            grupo=None,
            colegio_universidad=colegio_universidad,
            ocupacion=ocupacion
        )
        print(f"👨‍💻 Estudiante Técnico creado: {nombre_usuario}")

# Crear Estudiantes Regulares y Padres
def crear_estudiantes_regulares(cantidad):
    grupos = ['Sweet', 'Smart', 'Teens']
    for _ in range(cantidad):
        # Crear padre
        nombres_p = fake.first_name()
        apellidos_p = fake.last_name()
        ci_p = fake.unique.random_number(digits=7)
        direccion_p = fake.address()
        telefono_p = fake.phone_number()
        fecha_nacimiento_p = fake.date_of_birth(minimum_age=35, maximum_age=60)
        nombre_usuario_p = f"padre_{nombres_p.lower()}{random.randint(100,999)}"
        usuario_padre = crear_usuario(nombre_usuario_p, "12345678")

        padre = Padre.objects.create(
            usuario=usuario_padre,
            nombres=nombres_p,
            apellidos=apellidos_p,
            ci=ci_p,
            direccion=direccion_p,
            telefono=telefono_p,
            fecha_nacimiento=fecha_nacimiento_p
        )

        # Crear estudiante regular
        nombres = fake.first_name()
        apellidos = fake.last_name()
        ci = fake.unique.random_number(digits=7)
        direccion = fake.address()
        telefono = fake.phone_number()
        fecha_nacimiento = fake.date_of_birth(minimum_age=6, maximum_age=15)
        colegio = fake.company()
        ocupacion = "Estudiante"
        grupo = random.choice(grupos)
        nombre_usuario_e = f"{nombres.lower()}.{apellidos.lower()}.reg"
        usuario_est = crear_usuario(nombre_usuario_e, "12345678")

        Estudiante.objects.create(
            usuario=usuario_est,
            nombres=nombres,
            apellidos=apellidos,
            ci=ci,
            direccion=direccion,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            tipo="regular",
            grupo=grupo,
            colegio_universidad=colegio,
            ocupacion=ocupacion,
            padre=padre
        )
        print(f"👦 Estudiante Regular creado: {nombre_usuario_e} con padre {nombre_usuario_p}")

# Ejecutar
def run():
    print("🌟 Creando directivos...")
    crear_personal_admin(2, "directivo")

    print("🌟 Creando secretarias...")
    crear_personal_admin(3, "secretaria")

    print("🌟 Creando docentes...")
    crear_personal_admin(8, "docente")

    print("🌟 Creando estudiantes técnicos...")
    crear_estudiantes_tecnicos(15)

    print("🌟 Creando estudiantes regulares con padres...")
    crear_estudiantes_regulares(20)

    print("\n✅ Datos demo creados correctamente.")

