import json
import os

# directorio de datos
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
ESPACIOS_FILE = os.path.join(DATA_DIR, "espacios.json")
PLATOS_FILE = os.path.join(DATA_DIR, "platos.json")
RESERVAS_FILE = os.path.join(DATA_DIR, "reservas.json")

MAX_CAPACIDAD = 250

def cargar_datos(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# usuarios
def registrar_usuario(cedula, nombre, correo, rol="usuario"):
    usuarios = cargar_datos(USUARIOS_FILE)

    for u in usuarios:
        if u.get("cedula") == cedula:
            print("Cedula ya registrada")
            return

    usuarios.append({
        "cedula": cedula,
        "nombre": nombre,
        "correo": correo,
        "rol": rol
    })

    guardar_datos(USUARIOS_FILE, usuarios)
    print("Usuario registrado exitosamente")

def listar_usuarios():
    usuarios = cargar_datos(USUARIOS_FILE)
    if not usuarios:
        print("No hay usuarios registrados")
        return
    
    print(f"\n{'='*70}")
    print(f"{'CÉDULA':<15} | {'NOMBRE':<25} | {'CORREO':<25}")
    print(f"{'='*70}")
    for u in usuarios:
        print(f'{u.get("cedula","N/A"):<15} | {u["nombre"]:<25} | {u["correo"]:<25}')
    print(f"{'='*70}\n")

def existe_usuario(cedula):
    usuarios = cargar_datos(USUARIOS_FILE)
    for u in usuarios:
        if u.get("cedula") == cedula:
            return True
    return False

# espacios
def registrar_espacio(nombre, ubicacion, tipo, precio):
    espacios = cargar_datos(ESPACIOS_FILE)
    
    # Generar ID automático
    nuevo_id = 1
    if espacios:
        nuevo_id = max(e["id"] for e in espacios) + 1

    espacios.append({
        "id": nuevo_id,
        "nombre": nombre,
        "ubicacion": ubicacion,
        "tipo": tipo,
        "precio": precio,
        "ocupados": 0,
        "activo": True
    })

    guardar_datos(ESPACIOS_FILE, espacios)
    print(f"Espacio registrado exitosamente con ID: {nuevo_id}")

def listar_espacios():
    espacios = cargar_datos(ESPACIOS_FILE)
    if not espacios:
        print("No hay espacios registrados")
        return []
    
    print(f"\n{'='*80}")
    print(f"{'#':<5} | {'NOMBRE':<20} | {'TIPO':<15} | {'DISPONIBLES':<20} | {'PRECIO':<10}")
    print(f"{'='*80}")
    espacios_activos = []
    contador = 1
    for e in espacios:
        if e.get("activo", True):
            libres = MAX_CAPACIDAD - e["ocupados"]
            print(f'{contador:<5} | {e["nombre"]:<20} | {e["tipo"]:<15} | {libres}/{MAX_CAPACIDAD:<15} | ${e["precio"]:<9.2f}')
            espacios_activos.append(e)
            contador += 1
    print(f"{'='*80}\n")
    return espacios_activos

def obtener_espacio(id_espacio):
    for e in cargar_datos(ESPACIOS_FILE):
        if e["id"] == id_espacio and e.get("activo", True):
            return e
    return None

def actualizar_espacio(espacio_actualizado):
    espacios = cargar_datos(ESPACIOS_FILE)
    for i, e in enumerate(espacios):
        if e["id"] == espacio_actualizado["id"]:
            espacios[i] = espacio_actualizado
            break
    guardar_datos(ESPACIOS_FILE, espacios)

# platos
def registrar_plato(nombre, tipo, precio, cantidad):
    platos = cargar_datos(PLATOS_FILE)
    
    # Generar ID automático
    nuevo_id = 1
    if platos:
        nuevo_id = max(p["id"] for p in platos) + 1

    platos.append({
        "id": nuevo_id,
        "nombre": nombre,
        "tipo": tipo,
        "precio": precio,
        "cantidad": cantidad
    })

    guardar_datos(PLATOS_FILE, platos)
    print(f"Plato registrado exitosamente con ID: {nuevo_id}")

def listar_platos_por_tipo(tipo):
    platos = cargar_datos(PLATOS_FILE)
    lista = [p for p in platos if p["tipo"] == tipo and p["cantidad"] > 0]

    if not lista:
        return lista
    
    print(f"\n{'='*70}")
    print(f"Platos disponibles - {tipo.upper()}")
    print(f"{'='*70}")
    print(f"{'#':<5} | {'NOMBRE':<30} | {'PRECIO':<10} | {'STOCK':<10}")
    print(f"{'='*70}")
    for idx, p in enumerate(lista, 1):
        print(f'{idx:<5} | {p["nombre"]:<30} | ${p["precio"]:<9.2f} | {p["cantidad"]:<10}')
    print(f"{'='*70}\n")

    return lista

def actualizar_plato(plato_actualizado):
    platos = cargar_datos(PLATOS_FILE)
    for i, p in enumerate(platos):
        if p["id"] == plato_actualizado["id"]:
            platos[i] = plato_actualizado
            break
    guardar_datos(PLATOS_FILE, platos)

# reservas
def crear_reserva(cedula, num_espacio, fecha, hora_inicio, duracion_horas):
    if not existe_usuario(cedula):
        print("Usuario no registrado. Por favor regístrese primero.")
        return

    # Obtener lista de espacios activos
    espacios_activos = listar_espacios()
    if not espacios_activos:
        print("No hay espacios disponibles")
        return
    
    # Validar número de espacio
    if num_espacio < 1 or num_espacio > len(espacios_activos):
        print(f"Número de espacio inválido. Debe estar entre 1 y {len(espacios_activos)}")
        return
    
    espacio = espacios_activos[num_espacio - 1]

    if espacio["ocupados"] >= MAX_CAPACIDAD:
        print("No hay cupos disponibles en este espacio")
        return

    tipo = input("Tipo de comida (desayuno/almuerzo/merienda): ").lower().strip()
    if tipo not in ["desayuno", "almuerzo", "merienda"]:
        print("Tipo de comida no válido")
        return
    
    platos_disponibles = listar_platos_por_tipo(tipo)
    if not platos_disponibles:
        print("No hay platos disponibles para este tipo de comida")
        return

    platos_reserva = []
    total_comida = 0

    print("\nSeleccione los platos (ingrese 0 para finalizar)")
    while True:
        try:
            num_plato = int(input("Número del plato (0 para salir): "))
        except ValueError:
            print("Por favor ingrese un número válido")
            continue

        if num_plato == 0:
            break

        if num_plato < 1 or num_plato > len(platos_disponibles):
            print(f"Número inválido. Debe estar entre 1 y {len(platos_disponibles)}")
            continue

        plato = platos_disponibles[num_plato - 1]
        
        try:
            cantidad = int(input(f"Cantidad de '{plato['nombre']}': "))
        except ValueError:
            print("Por favor ingrese una cantidad válida")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0")
            continue

        if cantidad > plato["cantidad"]:
            print(f"Stock insuficiente. Solo hay {plato['cantidad']} disponibles")
            continue

        plato["cantidad"] -= cantidad
        subtotal = plato["precio"] * cantidad
        total_comida += subtotal

        platos_reserva.append({
            "nombre": plato["nombre"],
            "cantidad": cantidad,
            "precio_unitario": plato["precio"],
            "subtotal": subtotal
        })

        print(f"✓ Agregado: {cantidad} x {plato['nombre']} = ${subtotal:.2f}")

    if not platos_reserva:
        print("No se agregaron platos a la reserva")
        return

    reservas = cargar_datos(RESERVAS_FILE)
    
    # Generar ID automático
    nuevo_id = 1
    if reservas:
        nuevo_id = max(r["id"] for r in reservas) + 1

    total_reserva = espacio["precio"] + total_comida

    reservas.append({
        "id": nuevo_id,
        "cedula_usuario": cedula,
        "id_espacio": espacio["id"],
        "espacio": espacio["nombre"],
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "duracion_horas": duracion_horas,
        "platos": platos_reserva,
        "costo_espacio": espacio["precio"],
        "costo_alimentos": total_comida,
        "total": total_reserva,
        "estado": "Activa"
    })

    espacio["ocupados"] += 1

    # Actualizar datos en los archivos
    platos_todos = cargar_datos(PLATOS_FILE)
    for plato_mod in platos_disponibles:
        for i, p in enumerate(platos_todos):
            if p["id"] == plato_mod["id"]:
                platos_todos[i] = plato_mod
                break
    guardar_datos(PLATOS_FILE, platos_todos)
    
    actualizar_espacio(espacio)
    guardar_datos(RESERVAS_FILE, reservas)

    print(f"\n{'='*60}")
    print("✓ RESERVA CREADA EXITOSAMENTE")
    print(f"{'='*60}")
    print(f"ID de reserva: {nuevo_id}")
    print(f"Espacio: {espacio['nombre']}")
    print(f"Fecha: {fecha} a las {hora_inicio}")
    print(f"Duración: {duracion_horas} horas")
    print(f"Total a pagar: ${total_reserva:.2f}")
    print(f"{'='*60}\n")

def mostrar_reservas():
    reservas = cargar_datos(RESERVAS_FILE)
    if not reservas:
        print("No hay reservas registradas")
        return
    
    print(f"\n{'='*100}")
    print("LISTADO DE TODAS LAS RESERVAS")
    print(f"{'='*100}")
    
    for r in reservas:
        print(f"\nReserva #{r['id']}")
        print(f"  Cédula: {r['cedula_usuario']}")
        print(f"  Espacio: {r['espacio']}")
        print(f"  Fecha: {r['fecha']} - Hora: {r.get('hora_inicio', r.get('hora'))}")
        print(f"  Duración: {r.get('duracion_horas', r.get('duracion'))} horas")
        print(f"  Estado: {r['estado']}")
        print(f"  Total: ${r['total']:.2f}")
        print(f"  {'-'*50}")
    
    print(f"{'='*100}\n")

def ver_total_por_cedula(cedula):
    reservas = cargar_datos(RESERVAS_FILE)
    total_general = 0
    encontrado = False

    print(f"\n{'='*80}")
    print(f"RESUMEN DE RESERVAS - Cédula: {cedula}")
    print(f"{'='*80}")

    for r in reservas:
        if r["cedula_usuario"] == cedula:
            encontrado = True
            print(f"\n┌─ Reserva #{r['id']} {'─'*60}")
            print(f"│")
            print(f"│ Espacio: {r['espacio']}")
            print(f"│ Fecha: {r['fecha']}")
            print(f"│ Hora de inicio: {r.get('hora_inicio', r.get('hora'))}")
            print(f"│ Duración: {r.get('duracion_horas', r.get('duracion'))} horas")
            print(f"│ Estado: {r['estado']}")
            print(f"│")
            print(f"│ DESGLOSE DE COSTOS:")
            print(f"│ {'─'*70}")
            print(f"│")
            print(f"│ Costo del espacio: ${r.get('costo_espacio', 0):.2f}")
            print(f"│")
            
            if r["platos"]:
                print(f"│ Consumo de alimentos:")
                total_alimentos = 0
                for p in r["platos"]:
                    precio_unit = p.get('precio_unitario', 0)
                    print(f"│   • {p['nombre']:<30} x{p['cantidad']:<3} @ ${precio_unit:.2f} = ${p['subtotal']:.2f}")
                    total_alimentos += p['subtotal']
                print(f"│")
                print(f"│ Subtotal alimentos: ${total_alimentos:.2f}")
            else:
                print(f"│ Sin consumo de alimentos")
            
            print(f"│")
            print(f"│ {'─'*70}")
            print(f"└─ TOTAL DE ESTA RESERVA: ${r['total']:.2f}")
            print()
            
            total_general += r["total"]

    if not encontrado:
        print("No se encontraron reservas para esta cédula")
        print(f"{'='*80}\n")
        return

    print(f"{'='*80}")
    print(f"TOTAL A PAGAR POR TODAS LAS RESERVAS: ${total_general:.2f}")
    print(f"{'='*80}\n")

# menu
def menu():
    while True:
        print("\n" + "="*50)
        print("     SISTEMA DE RESERVAS DE ESPACIOS Y EVENTOS")
        print("="*50)
        print("1. Registrar usuario")
        print("2. Ver usuarios")
        print("3. Registrar espacio")
        print("4. Ver espacios")
        print("5. Registrar plato")
        print("6. Crear reserva")
        print("7. Ver todas las reservas")
        print("8. Ver total a pagar por usuario")
        print("0. Salir")
        print("="*50)

        op = input("Seleccione una opción: ").strip()

        if op == "1":
            print("\n--- REGISTRAR USUARIO ---")
            registrar_usuario(
                input("Cédula: ").strip(),
                input("Nombre completo: ").strip(),
                input("Correo electrónico: ").strip()
            )
        elif op == "2":
            print("\n--- LISTADO DE USUARIOS ---")
            listar_usuarios()
        elif op == "3":
            print("\n--- REGISTRAR ESPACIO ---")
            print(f"Capacidad máxima por espacio: {MAX_CAPACIDAD} personas")
            try:
                registrar_espacio(
                    input("Nombre del espacio: ").strip(),
                    input("Ubicación: ").strip(),
                    input("Tipo de evento: ").strip(),
                    float(input("Precio del espacio: $"))
                )
            except ValueError:
                print("Error: El precio debe ser un número válido")
        elif op == "4":
            print("\n--- LISTADO DE ESPACIOS ---")
            listar_espacios()
        elif op == "5":
            print("\n--- REGISTRAR PLATO ---")
            try:
                registrar_plato(
                    input("Nombre del plato: ").strip(),
                    input("Tipo (desayuno/almuerzo/merienda): ").strip().lower(),
                    float(input("Precio: $")),
                    int(input("Cantidad en stock: "))
                )
            except ValueError:
                print("Error: Verifique que el precio y cantidad sean números válidos")
        elif op == "6":
            print("\n--- CREAR RESERVA ---")
            espacios_disponibles = listar_espacios()
            if not espacios_disponibles:
                continue
            
            try:
                duracion_horas = int(input("Duración del evento (horas): "))
                if duracion_horas <= 0:
                    print("La duración debe ser mayor a 0")
                    continue

                crear_reserva(
                    input("Cédula del usuario: ").strip(),
                    int(input("Número del espacio: ")),
                    input("Fecha (dd/mm/yyyy): ").strip(),
                    input("Hora de inicio (HH:MM): ").strip(),
                    duracion_horas
                )
            except ValueError:
                print("Error: Verifique que los datos numéricos sean válidos")
        elif op == "7":
            print("\n--- TODAS LAS RESERVAS ---")
            mostrar_reservas()
        elif op == "8":
            print("\n--- TOTAL A PAGAR POR USUARIO ---")
            ver_total_por_cedula(input("Cédula del usuario: ").strip())
        elif op == "0":
            print("\n¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Por favor seleccione una opción del menú.")

if __name__ == "__main__":
    menu()