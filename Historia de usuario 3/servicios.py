
# ─────────────────────────────────────────────
# FUNCIÓN AUXILIAR: lambda para calcular subtotal
# ─────────────────────────────────────────────
subtotal = lambda p: p["precio"] * p["cantidad"]


# ─────────────────────────────────────────────
# CRUD
# ─────────────────────────────────────────────

def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.
        nombre (str): Nombre del producto.
        precio (float): Precio unitario (>= 0).
        cantidad (int): Unidades disponibles (>= 0).

    Retorna:
        bool: True si se agregó, False si el producto ya existe.
    """
    # Verificar si ya existe un producto con ese nombre (insensible a mayúsculas)
    if buscar_producto(inventario, nombre) is not None:
        print(f"   El producto '{nombre}' ya existe. Use 'Actualizar' para modificarlo.")
        return False

    # Crear el diccionario del producto y añadirlo a la lista
    producto = {"nombre": nombre, "precio": float(precio), "cantidad": int(cantidad)}
    inventario.append(producto)
    print(f"    Producto '{nombre}' agregado correctamente.")
    return True


def mostrar_inventario(inventario):
    """
    Imprime todos los productos del inventario en formato tabla.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.

    Retorna:
        None
    """
    if not inventario:
        print("    El inventario está vacío.")
        return

    # Encabezado de la tabla
    print(f"\n  {'#':<4} {'NOMBRE':<20} {'PRECIO':>10} {'CANTIDAD':>10} {'SUBTOTAL':>12}")
    print("  " + "-" * 60)

    for i, p in enumerate(inventario, 1):
        sub = subtotal(p)
        print(f"  {i:<4} {p['nombre']:<20} ${p['precio']:>9.2f} {p['cantidad']:>10} ${sub:>11.2f}")

    print("  " + "-" * 60)


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre (sin distinguir mayúsculas/minúsculas).

    Parámetros:
        inventario (list): Lista de diccionarios de productos.
        nombre (str): Nombre a buscar.

    Retorna:
        dict | None: El diccionario del producto si se encontró, None si no existe.
    """
    nombre_lower = nombre.strip().lower()
    for producto in inventario:
        if producto["nombre"].lower() == nombre_lower:
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o la cantidad de un producto existente.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.
        nombre (str): Nombre del producto a actualizar.
        nuevo_precio (float | None): Nuevo precio; None = no cambiar.
        nueva_cantidad (int | None): Nueva cantidad; None = no cambiar.

    Retorna:
        bool: True si se actualizó, False si no se encontró.
    """
    producto = buscar_producto(inventario, nombre)

    if producto is None:
        print(f"   Producto '{nombre}' no encontrado.")
        return False

    # Solo actualizar los campos que el usuario indicó
    if nuevo_precio is not None:
        producto["precio"] = float(nuevo_precio)
    if nueva_cantidad is not None:
        producto["cantidad"] = int(nueva_cantidad)

    print(f"    Producto '{nombre}' actualizado: precio=${producto['precio']:.2f}, cantidad={producto['cantidad']}")
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.
        nombre (str): Nombre del producto a eliminar.

    Retorna:
        bool: True si se eliminó, False si no existía.
    """
    producto = buscar_producto(inventario, nombre)

    if producto is None:
        print(f"    Producto '{nombre}' no encontrado.")
        return False

    inventario.remove(producto)
    print(f"    Producto '{nombre}' eliminado del inventario.")
    return True


# ─────────────────────────────────────────────
# ESTADÍSTICAS
# ─────────────────────────────────────────────

def calcular_estadisticas(inventario):
    """
    Calcula métricas globales del inventario.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.

    Retorna:
        dict con claves:
            unidades_totales (int)
            valor_total (float)
            producto_mas_caro (dict con nombre y precio)
            producto_mayor_stock (dict con nombre y cantidad)
        O None si el inventario está vacío.
    """
    if not inventario:
        return None

    # Suma de todas las cantidades
    unidades_totales = sum(p["cantidad"] for p in inventario)

    # Suma del valor (precio × cantidad) de cada producto usando la lambda
    valor_total = sum(subtotal(p) for p in inventario)

    # Producto con el precio unitario más alto
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])

    # Producto con más unidades en stock
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": {"nombre": producto_mas_caro["nombre"], "precio": producto_mas_caro["precio"]},
        "producto_mayor_stock": {"nombre": producto_mayor_stock["nombre"], "cantidad": producto_mayor_stock["cantidad"]},
    }


def mostrar_estadisticas(inventario):
    """
    Imprime en pantalla las estadísticas del inventario de forma legible.

    Parámetros:
        inventario (list): Lista de diccionarios de productos.

    Retorna:
        None
    """
    stats = calcular_estadisticas(inventario)

    if stats is None:
        print("    El inventario está vacío; no hay estadísticas que mostrar.")
        return

    print("\n  ╔══════════════════════════════════════╗")
    print("  ║       ESTADÍSTICAS DEL INVENTARIO    ║")
    print("  ╠══════════════════════════════════════╣")
    print(f"  ║  Unidades totales : {stats['unidades_totales']:>17} ║")
    print(f"  ║  Valor total      : ${stats['valor_total']:>16.2f} ║")
    print(f"  ║  Producto más caro: {stats['producto_mas_caro']['nombre'][:17]:>17} ║")
    print(f"  ║    → Precio       : ${stats['producto_mas_caro']['precio']:>16.2f} ║")
    print(f"  ║  Mayor stock      : {stats['producto_mayor_stock']['nombre'][:17]:>17} ║")
    print(f"  ║    → Cantidad     : {stats['producto_mayor_stock']['cantidad']:>17} ║")
    print("  ╚══════════════════════════════════════╝")

    # Mostrar subtotales por producto usando la lambda
    print("\n  Subtotales por producto:")
    for p in inventario:
        print(f"    • {p['nombre']:<18} → ${subtotal(p):>10.2f}")
