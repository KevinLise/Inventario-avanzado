import csv
import os


# ─────────────────────────────────────────────
# ENCABEZADO ESPERADO
# ─────────────────────────────────────────────
HEADER = ["nombre", "precio", "cantidad"]


# ─────────────────────────────────────────────
# GUARDAR CSV
# ─────────────────────────────────────────────

def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.
        ruta (str): Ruta del archivo destino (p. ej. 'datos/inventario.csv').
        incluir_header (bool): Si True, escribe la fila de encabezado.

    Retorna:
        bool: True si se guardó correctamente, False si hubo un error.
    """
    # Validar que el inventario no esté vacío antes de guardar
    if not inventario:
        print("    El inventario está vacío. No hay datos que guardar.")
        return False

    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        # Escribir el archivo CSV
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=HEADER)

            if incluir_header:
                writer.writeheader()      # Escribe: nombre,precio,cantidad

            writer.writerows(inventario)  # Escribe cada producto como fila

        print(f"    Inventario guardado en: {ruta}  ({len(inventario)} productos)")
        return True

    except PermissionError:
        # No se tienen permisos para escribir en esa ruta
        print(f"    Error de permisos: no se puede escribir en '{ruta}'.")
    except OSError as e:
        # Otros errores de sistema de archivos (disco lleno, ruta inválida, etc.)
        print(f"   Error al guardar el archivo: {e}")

    return False


# ─────────────────────────────────────────────
# CARGAR CSV
# ─────────────────────────────────────────────

def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV y los retorna como lista de diccionarios.

    Reglas de validación por fila:
        - Debe tener exactamente 3 columnas.
        - precio → float >= 0.
        - cantidad → int >= 0.
    Las filas inválidas se omiten y se contabilizan.

    Parámetros:
        ruta (str): Ruta del archivo CSV a leer.

    Retorna:
        tuple(list, int): (lista de productos válidos, número de filas omitidas)
        O (None, 0) si hubo un error crítico (archivo no encontrado, etc.).
    """
    productos = []
    filas_invalidas = 0

    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)

            # Validar que el encabezado sea correcto
            if reader.fieldnames is None or list(reader.fieldnames) != HEADER:
                print(f"    Encabezado inválido en '{ruta}'.")
                print(f"      Se esperaba: {','.join(HEADER)}")
                print(f"      Se encontró: {','.join(reader.fieldnames or [])}")
                return None, 0

            for num_fila, fila in enumerate(reader, start=2):  # start=2 porque fila 1 es el header
                try:
                    # Verificar que la fila tenga exactamente los 3 campos esperados
                    if len(fila) != 3:
                        raise ValueError("número incorrecto de columnas")

                    nombre = fila["nombre"].strip()
                    if not nombre:
                        raise ValueError("nombre vacío")

                    precio = float(fila["precio"])
                    if precio < 0:
                        raise ValueError("precio negativo")

                    cantidad = int(fila["cantidad"])
                    if cantidad < 0:
                        raise ValueError("cantidad negativa")

                    productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})

                except (ValueError, KeyError) as e:
                    # Fila inválida: la omitimos y acumulamos el contador
                    print(f"    Fila {num_fila} omitida ({e}): {dict(fila)}")
                    filas_invalidas += 1

    except FileNotFoundError:
        print(f"    Archivo no encontrado: '{ruta}'")
        return None, 0
    except UnicodeDecodeError:
        print(f"    Error de codificación al leer '{ruta}'. Asegúrese de que sea UTF-8.")
        return None, 0
    except Exception as e:
        print(f"    Error inesperado al leer '{ruta}': {e}")
        return None, 0

    return productos, filas_invalidas


# ─────────────────────────────────────────────
# INTEGRACIÓN CON EL INVENTARIO EN MEMORIA
# ─────────────────────────────────────────────

def aplicar_carga(inventario, productos_nuevos):
    """
    Aplica los productos cargados al inventario según la elección del usuario
    (sobrescribir o fusionar).

    Política de fusión:
        - Si el producto YA existe: se suma la cantidad y se actualiza al nuevo precio.
        - Si el producto NO existe: se agrega directamente.

    Parámetros:
        inventario (list): Lista actual en memoria (se modifica in-place).
        productos_nuevos (list): Productos leídos del CSV.

    Retorna:
        str: 'reemplazo' o 'fusión', según lo que eligió el usuario.
    """
    accion = ""

    while True:
        respuesta = input("  ¿Sobrescribir inventario actual? (S/N): ").strip().upper()

        if respuesta == "S":
            # Reemplazar toda la lista en memoria
            inventario.clear()
            inventario.extend(productos_nuevos)
            accion = "reemplazo"
            break

        elif respuesta == "N":
            # Política de fusión: suma de cantidad + actualización de precio
            print("    Política de fusión: si el producto ya existe,")
            print("      se SUMA la cantidad y se ACTUALIZA el precio al nuevo valor.")

            for nuevo in productos_nuevos:
                # Buscar si ya existe en el inventario actual
                existente = next(
                    (p for p in inventario if p["nombre"].lower() == nuevo["nombre"].lower()),
                    None
                )
                if existente:
                    existente["cantidad"] += nuevo["cantidad"]
                    existente["precio"] = nuevo["precio"]
                else:
                    inventario.append(nuevo)

            accion = "fusión"
            break

        else:
            print("    Opción inválida. Ingrese S o N.")

    return accion
