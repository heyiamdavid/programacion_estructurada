import json  # importar archivos json
import os  # importar para crear archivos y verificar si existen

# crear carpeta data si no existe
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# modulo para cargar datos
def cargar_datos(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

# modulo para guardar datos
def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Archivos
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
ESPACIOS_FILE = os.path.join(DATA_DIR, "espacios.json")
RECURSOS_FILE = os.path.join(DATA_DIR, "recursos.json")
RESERVAS_FILE = os.path.join(DATA_DIR, "reservas.json")

# modulo para registrar usuarios
def registrar_usuario(nombre, correo, rol="usuario"):
    usuarios = cargar_datos(USUARIOS_FILE)

    for u in usuarios:
        if u["correo"] == correo:
            print("Correo ya registrado")
            return

    usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "correo": correo,
        "rol": rol
    }

    usuarios.append(usuario)
    guardar_datos(USUARIOS_FILE, usuarios)
    print("Usuario registrado")

# modulo para obtener usuarios por id
def obtener_usuario(id_usuario):
    usuarios = cargar_datos(USUARIOS_FILE)
    for u in usuarios:
        if u["id"] == id_usuario:
            return u
    return None

# modulo para registrar espacios
def registrar_espacio(nombre, capacidad, ubicacion, tipo):
    espacios = cargar_datos(ESPACIOS_FILE)

    espacio = {
        "id": len(espacios) + 1,
        "nombre": nombre,
        "capacidad": capacidad,
        "ubicacion": ubicacion,
        "tipo": tipo,
        "activo": True
    }

    espacios.append(espacio)
    guardar_datos(ESPACIOS_FILE, espacios)
    print("Espacio registrado")

# modulo para listar espacios
def listar_espacios():
    espacios = cargar_datos(ESPACIOS_FILE)
    for e in espacios:
        estado = "Activo" if e["activo"] else "Inactivo"
        print(f'{e["id"]} - {e["nombre"]} ({estado})')

# modulo para registrar recursos
def registrar_recurso(nombre, espacio_id):
    recursos = cargar_datos(RECURSOS_FILE)

    recurso = {
        "id": len(recursos) + 1,
        "nombre": nombre,
        "espacio_id": espacio_id,
        "disponible": True
    }

    recursos.append(recurso)
    guardar_datos(RECURSOS_FILE, recursos)
    print("Recurso registrado")

# modulo para listar los recursos
def espacio_disponible(espacio_id, fecha, hora):
    reservas = cargar_datos(RESERVAS_FILE)
    for r in reservas:
        if (
            r["espacio_id"] == espacio_id and
            r["fecha"] == fecha and
            r["hora"] == hora and
            r["estado"] == "Activa"
        ):
            return False
    return True

# modulo para crear reservas
def crear_reserva(usuario_id, espacio_id, fecha, hora, duracion, recursos):
    if not espacio_disponible(espacio_id, fecha, hora):
        print("Espacio no disponible")
        return

    reservas = cargar_datos(RESERVAS_FILE)

    reserva = {
        "id": len(reservas) + 1,
        "usuario_id": usuario_id,
        "espacio_id": espacio_id,
        "fecha": fecha,
        "hora": hora,
        "duracion": duracion,
        "recursos": recursos,
        "estado": "Activa"
    }

    reservas.append(reserva)
    guardar_datos(RESERVAS_FILE, reservas)
    print("Reserva creada")

# modulo para cancelar reservas
def cancelar_reserva(id_reserva):
    reservas = cargar_datos(RESERVAS_FILE)
    for r in reservas:
        if r["id"] == id_reserva:
            r["estado"] = "Cancelada"
            guardar_datos(RESERVAS_FILE, reservas)
            print("Reserva cancelada")
            return
    print("Reserva no encontrada")

# modulo para mostrar reservas
def mostrar_reservas():
    reservas = cargar_datos(RESERVAS_FILE)
    for r in reservas:
        print(r)

# Menu principal
def menu():
    while True:
        print("\n--- SISTEMA DE RESERVAS ---")
        print("1. Registrar usuario")
        print("2. Registrar espacio")
        print("3. Registrar recurso")
        print("4. Crear reserva")
        print("5. Cancelar reserva")
        print("6. Ver reservas")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario(
                input("Nombre: "),
                input("Correo: "),
                input("Rol (admin/usuario): ")
            )
        elif opcion == "2":
            registrar_espacio(
                input("Nombre: "),
                int(input("Capacidad: ")),
                input("Ubicación: "),
                input("Tipo: ")
            )
        elif opcion == "3":
            registrar_recurso(
                input("Nombre del recurso: "),
                int(input("ID del espacio: "))
            )
        elif opcion == "4":
            crear_reserva(
                int(input("ID usuario: ")),
                int(input("ID espacio: ")),
                input("Fecha (YYYY-MM-DD): "),
                input("Hora (HH:MM): "),
                int(input("Duración (horas): ")),
                []
            )
        elif opcion == "5":
            cancelar_reserva(int(input("ID reserva: ")))
        elif opcion == "6":
            mostrar_reservas()
        elif opcion == "0":
            print("Saliendo del sistema")
            break
        else:
            print("Opción inválida")

# main principal
if __name__ == "__main__":
    menu()
