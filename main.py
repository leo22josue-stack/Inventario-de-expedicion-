import json
import os
from datetime import datetime

ARCHIVO_DATOS = "inventario.json"


def cargar_inventario():
    """Lee los productos guardados desde el archivo JSON. Si no existe, empieza vacío."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []


def guardar_inventario(inventario):
    """Guarda la lista de productos en el archivo JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


def agregar_producto(inventario):
    print("\n--- Agregar producto ---")
    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoría: ").strip()
    fecha_expedicion = input("Fecha de expedición/vencimiento (AAAA-MM-DD): ").strip()

    while True:
        cantidad_texto = input("Cantidad: ").strip()
        if cantidad_texto.isdigit():
            cantidad = int(cantidad_texto)
            break
        print("Por favor ingresa un número válido.")

    producto = {
        "nombre": nombre,
        "cantidad": cantidad,
        "categoria": categoria,
        "fecha_expedicion": fecha_expedicion,
    }

    inventario.append(producto)
    guardar_inventario(inventario)
    print(f"✅ Producto '{nombre}' agregado correctamente.\n")


def ver_inventario(inventario, lista_mostrar=None):
    print("\n--- Inventario de Expedición ---")
    datos = lista_mostrar if lista_mostrar is not None else inventario
    
    if not datos:
        print("No hay productos registrados.\n")
        return

    print(f"{'#':<4}{'Nombre':<20}{'Cantidad':<10}{'Categoría':<15}{'Fecha':<18}")
    print("-" * 67)
    for indice, producto in enumerate(datos, start=1):
        print(
            f"{indice:<4}{producto['nombre']:<20}{producto['cantidad']:<10}"
            f"{producto['categoria']:<15}{producto['fecha_expedicion']:<18}"
        )
    print()


def modificar_cantidad(inventario):
    """Permite aumentar o consumir suministros existentes."""
    ver_inventario(inventario)
    if not inventario:
        return

    numero_texto = input("Número del producto a modificar: ").strip()
    if not numero_texto.isdigit():
        print("Número no válido.\n")
        return

    indice = int(numero_texto) - 1
    if 0 <= indice < len(inventario):
        producto = inventario[indice]
        print(f"Modificando '{producto['nombre']}' (Cantidad actual: {producto['cantidad']})")
        print("1. Consumir / Reducir stock")
        print("2. Reabastecer / Aumentar stock")
        opcion = input("Elige una opción (1-2): ").strip()

        if opcion in ["1", "2"]:
            cant_texto = input("Cantidad a ajustar: ").strip()
            if cant_texto.isdigit():
                cambio = int(cant_texto)
                if opcion == "1":
                    if cambio > producto["cantidad"]:
                        print("⚠️ No puedes consumir más de lo que tienes en stock.\n")
                        return
                    producto["cantidad"] -= cambio
                else:
                    producto["cantidad"] += cambio

                guardar_inventario(inventario)
                print(f"✅ Stock actualizado. Nueva cantidad de '{producto['nombre']}': {producto['cantidad']}\n")
            else:
                print("Cantidad no válida.\n")
        else:
            print("Opción inválida.\n")
    else:
        print("Ese número no existe en la lista.\n")


def buscar_producto(inventario):
    """Filtra los productos por término de búsqueda (nombre o categoría)."""
    if not inventario:
        print("\nEl inventario está vacío.\n")
        return

    termino = input("\nIngrese nombre o categoría a buscar: ").strip().lower()
    resultados = [
        p for p in inventario 
        if termino in p["nombre"].lower() or termino in p["categoria"].lower()
    ]

    print(f"\n--- Resultados de búsqueda para '{termino}' ---")
    ver_inventario(inventario, lista_mostrar=resultados)


def verificar_alertas(inventario):
    """Muestra alertas de suministros en stock crítico o próximos a su fecha."""
    if not inventario:
        print("\nEl inventario está vacío.\n")
        return

    print("\n--- ⚠️ Alertas de Expedición ---")
    alertas_stock = [p for p in inventario if p["cantidad"] <= 2]
    
    if alertas_stock:
        print("🚨 Stock crítico (2 unidades o menos):")
        for p in alertas_stock:
            print(f"  - {p['nombre']}: {p['cantidad']} unidades restantes ({p['categoria']})")
    else:
        print("✅ Niveles de stock aceptables en todos los productos.")

    hoy_str = datetime.now().strftime("%Y-%m-%d")
    vencidos_o_proximos = [p for p in inventario if p["fecha_expedicion"] <= hoy_str and p["fecha_expedicion"] != ""]
    
    if vencidos_o_proximos:
        print("\n📅 Productos en fecha límite o vencidos:")
        for p in vencidos_o_proximos:
            print(f"  - {p['nombre']} (Fecha registrada: {p['fecha_expedicion']})")
    print()


def eliminar_producto(inventario):
    ver_inventario(inventario)
    if not inventario:
        return

    numero_texto = input("Número del producto a eliminar: ").strip()
    if not numero_texto.isdigit():
        print("Número no válido.\n")
        return

    indice = int(numero_texto) - 1
    if 0 <= indice < len(inventario):
        eliminado = inventario.pop(indice)
        guardar_inventario(inventario)
        print(f"🗑️ Producto '{eliminado['nombre']}' eliminado.\n")
    else:
        print("Ese número no existe en la lista.\n")


def mostrar_menu():
    print("=== Inventario de Expedición ===")
    print("1. Agregar producto")
    print("2. Ver inventario completo")
    print("3. Modificar / Consumir stock")
    print("4. Buscar por nombre o categoría")
    print("5. Reporte de alertas (Stock bajo y fechas)")
    print("6. Eliminar producto")
    print("7. Salir")


def main():
    inventario = cargar_inventario()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-7): ").strip()

        if opcion == "1":
            agregar_producto(inventario)
        elif opcion == "2":
            ver_inventario(inventario)
        elif opcion == "3":
            modificar_cantidad(inventario)
        elif opcion == "4":
            buscar_producto(inventario)
        elif opcion == "5":
            verificar_alertas(inventario)
        elif opcion == "6":
            eliminar_producto(inventario)
        elif opcion == "7":
            print("¡Expedición finalizada! Datos guardados.")
            break
        else:
            print("Opción no válida, intenta de nuevo.\n")


if __name__ == "__main__":
    main()