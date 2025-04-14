import sys

from package import Model, View, ViewModel

# eliminar ---
"""
def crear_datos_ejemplo():    
    # Agregar componentes al inventario de las tiendas
    tienda_bosquemar.agregar_componente(ram, 10)
    tienda_bosquemar.agregar_componente(procesador, 5)
    tienda_mirasol.agregar_componente(ssd, 8)
    tienda_vallevolcanes.agregar_componente(ram, 15)
    tienda_vallevolcanes.agregar_componente(ssd, 10)
    
    # Lista de tiendas y vendedores
    tiendas = [tienda_bosquemar, tienda_mirasol, tienda_vallevolcanes]
    vendedores = [vendedor1, vendedor2, vendedor3]
    
    return tiendas, vendedores
"""
# ---

if __name__ == "__main__":
    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    viewmodel = ViewModel(model)
    view = View(viewmodel)

    view.show()
    # dudar de dejarlo -
    #  Crear datos de ejemplo
    # tiendas, vendedores = crear_datos_ejemplo()
    # Crear controladores
    # controlador_inventario = InventarioController(tiendas)
    # controlador_ventas = VentaController()
    # Crear y mostrar la interfaz
    # ventana = InterfazTienda(controlador_inventario, controlador_ventas, tiendas, vendedores)
    # ventana.show()
    # ---

    sys.exit(app.exec())