"""
Sistema básico de inventario con POO en Python.

Clases:
- Producto: representa un producto con nombre, precio y cantidad.
- Inventario: gestiona una colección de productos.

Incluye validaciones, manejo de excepciones y un menú interactivo.
"""

from __future__ import annotations

from typing import List


class Producto:
    """Representa un producto del inventario."""

    def __init__(self, nombre: str, precio: float, cantidad: int) -> None:
        """Inicializa un producto con validaciones de tipo y valor.

        Reglas:
        - nombre: str no vacío
        - precio: number >= 0
        - cantidad: int >= 0
        """
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser de tipo str.")
        nombre_normalizado = nombre.strip()
        if not nombre_normalizado:
            raise ValueError("El nombre no puede estar vacío.")

        # Acepta int o float para precio, pero almacena como float
        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            raise TypeError("El precio debe ser numérico (int o float).")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        # cantidad debe ser int no negativo (excluye bool)
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un entero.")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        self._nombre: str = nombre_normalizado
        self._precio: float = float(precio)
        self._cantidad: int = int(cantidad)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio(self) -> float:
        return self._precio

    @property
    def cantidad(self) -> int:
        return self._cantidad

    def actualizar_precio(self, nuevo_precio: float) -> None:
        """Actualiza el precio validando que sea positivo (> 0).

        Acepta int o float; almacena como float.
        """
        if not isinstance(nuevo_precio, (int, float)) or isinstance(nuevo_precio, bool):
            raise TypeError("El nuevo precio debe ser numérico (int o float).")
        if nuevo_precio <= 0:
            raise ValueError("El nuevo precio debe ser mayor que cero.")
        self._precio = float(nuevo_precio)

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        """Actualiza la cantidad validando que sea >= 0."""
        if not isinstance(nueva_cantidad, int) or isinstance(nueva_cantidad, bool):
            raise TypeError("La nueva cantidad debe ser un entero.")
        if nueva_cantidad < 0:
            raise ValueError("La nueva cantidad no puede ser negativa.")
        self._cantidad = int(nueva_cantidad)

    def calcular_valor_total(self) -> float:
        """Devuelve el valor total (precio × cantidad)."""
        return self._precio * self._cantidad

    def __str__(self) -> str:
        return (
            f"Producto(nombre='{self._nombre}', precio={self._precio:.2f}, "
            f"cantidad={self._cantidad}, valor_total={self.calcular_valor_total():.2f})"
        )


class Inventario:
    """Gestiona una colección de productos."""

    def __init__(self) -> None:
        self._productos: List[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto si no existe otro con el mismo nombre (case-insensitive).

        Lanza:
        - TypeError: si el argumento no es Producto
        - ValueError: si ya existe un producto con el mismo nombre
        """
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar instancias de Producto.")

        try:
            self.buscar_producto(producto.nombre)
        except KeyError:
            self._productos.append(producto)
            return
        raise ValueError(f"Ya existe un producto con el nombre '{producto.nombre}'.")

    def buscar_producto(self, nombre: str) -> Producto:
        """Busca un producto por nombre (case-insensitive).

        Lanza KeyError si no se encuentra.
        """
        if not isinstance(nombre, str):
            raise TypeError("El nombre de búsqueda debe ser de tipo str.")
        nombre_normalizado = nombre.strip()
        if not nombre_normalizado:
            raise ValueError("El nombre de búsqueda no puede estar vacío.")

        for producto in self._productos:
            if producto.nombre.lower() == nombre_normalizado.lower():
                return producto
        raise KeyError(f"Producto con nombre '{nombre_normalizado}' no encontrado.")

    def calcular_valor_inventario(self) -> float:
        """Suma el valor total de todos los productos."""
        return sum(p.calcular_valor_total() for p in self._productos)

    def listar_productos(self) -> List[Producto]:
        """Devuelve una copia superficial de la lista de productos."""
        return list(self._productos)


def menu_principal(inventario: Inventario) -> None:
    """Muestra el menú interactivo y procesa la entrada del usuario."""
    opciones = {
        "1": "Agregar producto",
        "2": "Buscar producto",
        "3": "Listar productos",
        "4": "Calcular valor total del inventario",
        "5": "Salir",
    }

    while True:
        print("\n===== Sistema de Inventario =====")
        for clave, etiqueta in opciones.items():
            print(f"{clave}. {etiqueta}")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                nombre = input("Nombre del producto: ").strip()
                precio_str = input("Precio (ej. 199.99): ").strip()
                cantidad_str = input("Cantidad (entero >= 0): ").strip()

                # Conversión básica, validaciones profundas dentro de Producto
                precio = float(precio_str)
                cantidad = int(cantidad_str)

                producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
                inventario.agregar_producto(producto)
                print("Producto agregado correctamente.")
            except (ValueError, TypeError) as exc:
                print(f"Error al agregar producto: {exc}")
            except Exception as exc:  # Como salvaguarda final
                print(f"Ocurrió un error inesperado: {exc}")

        elif opcion == "2":
            try:
                nombre_busqueda = input("Nombre a buscar: ").strip()
                producto_encontrado = inventario.buscar_producto(nombre_busqueda)
                print(producto_encontrado)
            except (ValueError, TypeError, KeyError) as exc:
                print(f"Error en la búsqueda: {exc}")

        elif opcion == "3":
            productos = inventario.listar_productos()
            if not productos:
                print("No hay productos en el inventario.")
            else:
                print("\nListado de productos:")
                for indice, prod in enumerate(productos, start=1):
                    print(f"{indice}. {prod}")

        elif opcion == "4":
            try:
                total = inventario.calcular_valor_inventario()
                print(f"Valor total del inventario: {total:.2f}")
            except Exception as exc:
                print(f"Ocurrió un error al calcular el total: {exc}")

        elif opcion == "5":
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    inventario_app = Inventario()
    menu_principal(inventario_app)


