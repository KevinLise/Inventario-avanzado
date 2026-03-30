# ──────────────────────────────────────────
# PROGRAMA: Gestión de Héroes (CRUD + JSON)
# La información se almacena en un diccionario
# en memoria y se persiste en un archivo JSON.
# ──────────────────────────────────────────

import json
import os

# Archivo donde se guarda la información
ARCHIVO = "heroes.json"

# ──────────────────────────────────────────
# CARGA INICIAL
# Si el archivo JSON existe, carga los datos
# en el diccionario. Si no, usa datos base.
# ──────────────────────────────────────────

def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return {int(k): v for k, v in datos.items()}
    return {
        1: {"id": 100327560, "nombre": "Spiderman",   "edad": "21",   "power": "Perseverance"},
        2: {"id": 100326570, "nombre": "Ghos Raider", "edad": "36",   "power": "Absolute Justice"},
        3: {"id": 100326590, "nombre": "Goku Black",  "edad": "1000", "power": "Super Saiyan Rose Black"},
    }

def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in heroe.items()}, f, indent=4, ensure_ascii=False)
    print(f"(Guardado en '{ARCHIVO}')")

# Cargar datos al iniciar el programa
heroe = cargar_datos()

# ──────────────────────────────────────────
# FUNCIONES CRUD
# ──────────────────────────────────────────

# READ: Mostrar todos los héroes del diccionario
def mostrar_heroes():
    if len(heroe) == 0:
        print("No hay heroes registrados.")
        return
    print("\n── Lista de heroes ──")
    for llave, datos in heroe.items():
        print(f"\n  Slot   : {llave}")
        print(f"  ID     : {datos['id']}")
        print(f"  Nombre : {datos['nombre']}")
        print(f"  Edad   : {datos['edad']}")
        print(f"  Power  : {datos['power']}")
    print()

# CREATE: Agregar un nuevo héroe al diccionario y guardar
def agregar_heroe():
    nueva_llave = max(heroe.keys(), default=0) + 1
    print(f"\nNuevo heroe ocupara el slot {nueva_llave}")

    nuevo_id   = input("ID      : ").strip()
    nuevo_nom  = input("Nombre  : ").strip()
    nueva_edad = input("Edad    : ").strip()
    nuevo_pow  = input("Power   : ").strip()

    heroe[nueva_llave] = {
        "id":     nuevo_id,
        "nombre": nuevo_nom,
        "edad":   nueva_edad,
        "power":  nuevo_pow
    }
    guardar_datos()
    print(f"Heroe '{nuevo_nom}' agregado en slot {nueva_llave}.")

# UPDATE: Actualizar campos de un héroe existente y guardar
def actualizar_heroe():
    mostrar_heroes()
    if len(heroe) == 0:
        return

    try:
        llave = int(input("Numero de slot a actualizar: "))
        if llave not in heroe:
            print("Slot no encontrado.")
            return
    except ValueError:
        print("Ingresa un numero valido.")
        return

    datos = heroe[llave]
    print(f"\nActualizando: {datos['nombre']} (Enter para conservar valor actual)")

    nuevo_id   = input(f"  ID     [{datos['id']}]: ").strip()
    nuevo_nom  = input(f"  Nombre [{datos['nombre']}]: ").strip()
    nueva_edad = input(f"  Edad   [{datos['edad']}]: ").strip()
    nuevo_pow  = input(f"  Power  [{datos['power']}]: ").strip()

    if nuevo_id:
        heroe[llave]["id"]     = nuevo_id
    if nuevo_nom:
        heroe[llave]["nombre"] = nuevo_nom
    if nueva_edad:
        heroe[llave]["edad"]   = nueva_edad
    if nuevo_pow:
        heroe[llave]["power"]  = nuevo_pow

    guardar_datos()
    print(f"Heroe en slot {llave} actualizado correctamente.")

# DELETE: Eliminar un héroe del diccionario y guardar
def eliminar_heroe():
    mostrar_heroes()
    if len(heroe) == 0:
        return

    try:
        llave = int(input("Numero de slot a eliminar: "))
        if llave in heroe:
            nombre = heroe[llave]["nombre"]
            confirmar = input(f"¿Seguro que deseas eliminar '{nombre}'? (s/n): ").strip().lower()
            if confirmar == "s":
                del heroe[llave]
                guardar_datos()
                print(f"Heroe '{nombre}' eliminado.")
            else:
                print("Eliminacion cancelada.")
        else:
            print("Slot no encontrado.")
    except ValueError:
        print("Ingresa un numero valido.")

# READ (filtrado): Buscar por ID exacto
def buscar_por_id():
    try:
        busqueda_id = int(input("Ingresa el ID a buscar: "))
        encontrado = None
        for llave, datos in heroe.items():
            if int(datos["id"]) == busqueda_id:
                encontrado = (llave, datos)
                break
        if encontrado:
            llave, datos = encontrado
            print(f"\n  Slot   : {llave}")
            print(f"  ID     : {datos['id']}")
            print(f"  Nombre : {datos['nombre']}")
            print(f"  Edad   : {datos['edad']}")
            print(f"  Power  : {datos['power']}")
        else:
            print("No se encontro un heroe con ese ID.")
    except ValueError:
        print("Ingresa un numero valido.")

# READ (filtrado): Buscar por nombre — parcial e insensible a mayúsculas
# Ejemplo: buscar "goku" encuentra "Goku Black"
# Los resultados se acumulan en una lista antes de imprimirse
def buscar_por_nombre():
    termino = input("Ingresa el nombre (o parte del nombre): ").strip().lower()

    if termino == "":
        print("No ingresaste ningun texto.")
        return

    # Recorre el diccionario y acumula coincidencias en una lista
    resultados = []
    for llave, datos in heroe.items():
        if termino in datos["nombre"].lower():
            resultados.append((llave, datos))

    if len(resultados) == 0:
        print(f"No se encontro ningun heroe con el nombre '{termino}'.")
        return

    print(f"\n── {len(resultados)} resultado(s) para '{termino}' ──")
    for llave, datos in resultados:
        print(f"\n  Slot   : {llave}")
        print(f"  ID     : {datos['id']}")
        print(f"  Nombre : {datos['nombre']}")
        print(f"  Edad   : {datos['edad']}")
        print(f"  Power  : {datos['power']}")

# ──────────────────────────────────────────
# MENU PRINCIPAL
# ──────────────────────────────────────────

while True:
    print("\n════════════════════════")
    print("     MENU DE HEROES     ")
    print("════════════════════════")
    print("1. Mostrar todos     (READ)")
    print("2. Agregar heroe     (CREATE)")
    print("3. Actualizar        (UPDATE)")
    print("4. Eliminar heroe    (DELETE)")
    print("5. Buscar por ID     (READ)")
    print("6. Buscar por nombre (READ)")
    print("7. Salir")

    opcion = input("\nElige una opcion: ").strip()

    if opcion == "1":
        mostrar_heroes()
    elif opcion == "2":
        agregar_heroe()
    elif opcion == "3":
        actualizar_heroe()
    elif opcion == "4":
        eliminar_heroe()
    elif opcion == "5":
        buscar_por_id()
    elif opcion == "6":
        buscar_por_nombre()
    elif opcion == "7":
        print("Saliendo...")
        break
    else:
        print("Opcion invalida, intenta de nuevo.")

# ──────────────────────────────────────────
# RESUMEN DEL PROGRAMA:
# - heroe: diccionario en memoria (estructura principal)
# - heroes.json: archivo de persistencia en disco
# - cargar_datos(): lee el JSON al iniciar
# - guardar_datos(): escribe el JSON después de cada cambio
# - CRUD completo: mostrar, agregar, actualizar, eliminar
# - Búsqueda por ID (exacta) y por nombre (parcial, sin importar mayúsculas)
# ──────────────────────────────────────────
