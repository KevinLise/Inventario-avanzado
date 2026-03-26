# Importar los módulos propios del proyecto
from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    mostrar_estadisticas,
)
from archivos import guardar_csv, cargar_csv, aplicar_carga


# ─────────────────────────────────────────────
# FUNCIONES DE ENTRADA VALIDADA
# ─────────────────────────────────────────────

def pedir_float(mensaje):
    """
    Solicita al usuario un número decimal no negativo.

    Parámetros:
        mensaje (str): Texto que se muestra al usuario.

    Retorna:
        float: Valor ingresado y validado.
    """
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("    El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("    Debe ingresar un número válido (p. ej. 12.50).")


def pedir_int(mensaje):
    """
    Solicita al usuario un número entero no negativo.

    Parámetros:
        mensaje (str): Texto que se muestra al usuario.

    Retorna:
        int: Valor ingresado y validado.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("    El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("    Debe ingresar un número entero (p. ej. 10).")


def pedir_nombre(mensaje):
    """
    Solicita al usuario un nombre no vacío.

    Parámetros:
        mensaje (str): Texto a mostrar.

    Retorna:
        str: Nombre sin espacios al inicio/fin.
    """
    while True:
        nombre = input(mensaje).strip()
        if nombre:
            return nombre
        print("    El nombre no puede estar vacío.")


# ─────────────────────────────────────────────
# OPCIONES DEL MENÚ
# ─────────────────────────────────────────────

def opcion_agregar(inventario):
    """Flujo para agregar un producto nuevo."""
    print("\n  ── AGREGAR PRODUCTO ──")
    nombre   = pedir_nombre("  Nombre   : ")
    precio   = pedir_float("  Precio   : $")
    cantidad = pedir_int("  Cantidad : ")
    agregar_producto(inventario, nombre, precio, cantidad)


def opcion_mostrar(inventario):
    """Muestra todos los productos del inventario."""
    print("\n  ── INVENTARIO ACTUAL ──")
    mostrar_inventario(inventario)


def opcion_buscar(inventario):
    """Flujo para buscar un producto por nombre."""
    print("\n  ── BUSCAR PRODUCTO ──")
    nombre = pedir_nombre("  Nombre a buscar: ")
    producto = buscar_producto(inventario, nombre)

    if producto:
        print(f"\n  Producto encontrado:")
        print(f"    Nombre   : {producto['nombre']}")
        print(f"    Precio   : ${producto['precio']:.2f}")
        print(f"    Cantidad : {producto['cantidad']}")
    else:
        print(f"    No se encontró el producto '{nombre}'.")


def opcion_actualizar(inventario):
    """Flujo para actualizar precio y/o cantidad de un producto."""
    print("\n  ── ACTUALIZAR PRODUCTO ──")
    nombre = pedir_nombre("  Nombre del producto: ")

    # Verificar que el producto exista antes de pedir los nuevos valores
    if buscar_producto(inventario, nombre) is None:
        print(f"    Producto '{nombre}' no encontrado.")
        return

    print("  (Deje en blanco para no cambiar el valor)")

    # Precio: opcional
    entrada_precio = input("  Nuevo precio   : $").strip()
    nuevo_precio = None
    if entrada_precio:
        try:
            nuevo_precio = float(entrada_precio)
            if nuevo_precio < 0:
                print("    Precio negativo ignorado.")
                nuevo_precio = None
        except ValueError:
            print("    Precio inválido ignorado.")

    # Cantidad: opcional
    entrada_cantidad = input("  Nueva cantidad : ").strip()
    nueva_cantidad = None
    if entrada_cantidad:
        try:
            nueva_cantidad = int(entrada_cantidad)
            if nueva_cantidad < 0:
                print("    Cantidad negativa ignorada.")
                nueva_cantidad = None
        except ValueError:
            print("    Cantidad inválida ignorada.")

    actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)


def opcion_eliminar(inventario):
    """Flujo para eliminar un producto."""
    print("\n  ── ELIMINAR PRODUCTO ──")
    nombre = pedir_nombre("  Nombre del producto: ")

    # Pedir confirmación antes de eliminar
    confirmar = input(f"  ¿Confirmar eliminación de '{nombre}'? (S/N): ").strip().upper()
    if confirmar == "S":
        eliminar_producto(inventario, nombre)
    else:
        print("   Operación cancelada.")


def opcion_estadisticas(inventario):
    """Muestra estadísticas del inventario."""
    mostrar_estadisticas(inventario)


def opcion_guardar(inventario):
    """Flujo para guardar el inventario en un CSV."""
    print("\n  ── GUARDAR CSV ──")
    ruta = input("  Ruta del archivo (p. ej. datos/inventario.csv): ").strip()
    if not ruta:
        ruta = "inventario.csv"  # valor por defecto
    guardar_csv(inventario, ruta)


def opcion_cargar(inventario):
    """Flujo para cargar un CSV al inventario."""
    print("\n  ── CARGAR CSV ──")
    ruta = input("  Ruta del archivo CSV: ").strip()
    if not ruta:
        print("    Debe indicar una ruta.")
        return

    # Cargar y validar el archivo
    productos_nuevos, filas_invalidas = cargar_csv(ruta)

    if productos_nuevos is None:
        # Error crítico ya reportado dentro de cargar_csv
        return

    if not productos_nuevos:
        print("    No se encontraron productos válidos en el archivo.")
        if filas_invalidas:
            print(f"      ({filas_invalidas} filas inválidas omitidas)")
        return

    # Mostrar resumen previo
    print(f"\n  Se encontraron {len(productos_nuevos)} productos válidos.")
    if filas_invalidas:
        print(f"    {filas_invalidas} filas inválidas omitidas.")

    # Preguntar al usuario cómo integrar los datos
    accion = aplicar_carga(inventario, productos_nuevos)

    # Resumen final
    print(f"\n    Acción realizada: {accion.upper()}")
    print(f"    Productos cargados: {len(productos_nuevos)}")
    print(f"    Filas inválidas omitidas: {filas_invalidas}")
    print(f"    Total en inventario ahora: {len(inventario)}")


# ─────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────

MENU = """
  ╔══════════════════════════════════════╗
  ║      SISTEMA DE INVENTARIO           ║
  ╠══════════════════════════════════════╣
  ║  1. Agregar producto                 ║
  ║  2. Mostrar inventario               ║
  ║  3. Buscar producto                  ║
  ║  4. Actualizar producto              ║
  ║  5. Eliminar producto                ║
  ║  6. Estadísticas                     ║
  ║  7. Guardar CSV                      ║
  ║  8. Cargar CSV                       ║
  ║  9. Salir                            ║
  ╚══════════════════════════════════════╝"""

# Diccionario que mapea cada opción numérica a su función correspondiente
OPCIONES = {
    "1": opcion_agregar,
    "2": opcion_mostrar,
    "3": opcion_buscar,
    "4": opcion_actualizar,
    "5": opcion_eliminar,
    "6": opcion_estadisticas,
    "7": opcion_guardar,
    "8": opcion_cargar,
}


def main():
    """
    Función principal: inicializa el inventario y ejecuta el bucle del menú.
    El programa permanece activo hasta que el usuario seleccione la opción 9.
    """
    # Inventario en memoria: lista de diccionarios
    inventario = []

    print("\n  Bienvenido al Sistema de Inventario")

    while True:
        print(MENU)

        opcion = input("  Seleccione una opción (1-9): ").strip()

        if opcion == "9":
            # Preguntar si desea guardar antes de salir
            guardar = input("  ¿Desea guardar el inventario antes de salir? (S/N): ").strip().upper()
            if guardar == "S":
                opcion_guardar(inventario)
            print("\n  ¡Hasta luego!\n")
            break

        elif opcion in OPCIONES:
            # Llamar a la función correspondiente; capturar cualquier excepción no prevista
            try:
                OPCIONES[opcion](inventario)
            except Exception as e:
                # Ningún error del usuario debe cerrar la aplicación
                print(f"    Ocurrió un error inesperado: {e}")
                print("      Volviendo al menú principal...")

        else:
            print("    Opción inválida. Ingrese un número del 1 al 9.")

        # Pausa para que el usuario lea el resultado antes de limpiar la pantalla
        input("\n  Presione ENTER para continuar...")


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
