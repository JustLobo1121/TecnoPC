import os
from PySide6 import QtUiTools
from PySide6.QtWidgets import QMessageBox

class BaseWidget(QtUiTools.QUiLoader):
    def __init__(self, path):
        super().__init__()
        self._ui_widget = self.load(path)
    
    def show(self):
        self._ui_widget.show()

    @property
    def ui_widget(self):
        return self._ui_widget
    
class View(BaseWidget):
    def __init__(self, viewmodel):
        super().__init__(os.path.join("ui","main.ui"))
        self._viewmodel = viewmodel

        # vars
        self._tabs = self._ui_widget.tabWidget
        self._tabs.currentChanged.connect(self._handle_dinamic_data)
        self._data = self._viewmodel.get_data()

        self._shops = self._data["Tiendas"]
        self._salesmans = self._data["Vendedores"]
        self._components = self._data["Componentes"]

        self._type = ["Todos", "RAM", "Procesador", "Tarjeta Gráfica", "Placa Madre", "SSD", "Refrigeración", "Disipador de Calor"]

        # adding data
        for shop in self._shops:
            self._ui_widget.shopComboBox.addItem(f"{shop['nombre']} - {shop['direccion']}", shop)
        for item in self._type:
            self._ui_widget.type_comboBox.addItem(item, item)
        self._ui_widget.inventory_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Marca", "Precio", "Stock", "Tienda"
        ])


        # btns
        # (con los botones tienen que conectar y las funcionalidades)
        # - tab 1
        # self._ui_widget.buscar_btn
        # self._ui_widget.add_component_btn
        # self._ui_widget.edit_component_btn
        # self._ui_widget.transfer_btn
        # - tab 2
        # self._ui_widget.new_sell_btn
        # self._ui_widget.add_item_btn
        # self._ui_widget.cancel_btn
        # self._ui_widget.end_sell_btn
        # - tab 3
        # self._ui_widget.add_saleman_btn
        # self._ui_widget.edit_saleman_btn
        # self._ui_widget.view_stats_btn
        # self._ui_widget.calculation_comission

    def _handle_dinamic_data(self, tab: int): # es para hacer que los datos aparescan en el tab 2,3
        print(f"Tab {tab} selected")
        
        if tab == 1:
            for salesman in self._salesmans:
                self._ui_widget.seller_comboBox.addItem(f"{salesman['nombre']} - {salesman['tienda']}", salesman)
        
            for component in self._components:
                self._ui_widget.components_comboBox.addItem(f"{component['nombre']} - {component['tipo']}", component)
            self._ui_widget.item_sale_table.setHorizontalHeaderLabels(["ID", "Componente", "Precio", "Cantidad", "Subtotal"])
            self._ui_widget.history_sale_table.setHorizontalHeaderLabels(["ID", "Fecha", "Vendedor", "Tienda", "Items", "Total"])
        elif tab == 2:
            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            for i, month in enumerate(months, 1):
                self._ui_widget.month_comboBox.addItem(month, i)
            for year in range(2023, 2026):
                self._ui_widget.year_comboBox.addItem(str(year), year)
            self._ui_widget.comission_table.setHorizontalHeaderLabels(["Vendedor", "Ventas Totales", "# Ventas", "Comision"])
            self._ui_widget.salesman_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Teléfono", "Tienda"])

    # Métodos de acción para los distintos eventos (archivo de origen: interfaz_tienda.py)
    
    def buscar_componentes(self):
        """Ejecuta la búsqueda de componentes según los filtros."""
        # Aquí se implementaría la lógica de búsqueda
        QMessageBox.information(self.ui_widget, "Búsqueda", "Función de búsqueda no implementada.")
    
    def mostrar_form_agregar_componente(self):
        """Muestra el formulario para agregar un nuevo componente."""
        QMessageBox.information(self.ui_widget, "Agregar Componente",
                               "Función para agregar componente no implementada.")
    
    def iniciar_nueva_venta(self):
        """Inicia una nueva venta."""
        if not self.ui_widget.cliente_edit.text():
            QMessageBox.warning(self.ui_widget, "Error", "Debe ingresar un cliente.")
            return
        
        # Obtener vendedor y tienda seleccionados
        vendedor = self.ui_widget.seller_comboBox.currentData()
        tienda = self.ui_widget.shopComboBox.currentData()
        
        # Crear nueva venta
        # Aquí se implementaría la lógica con el controlador_ventas
        
        self.ui_widget.label_6.setText(f"Venta en curso: Cliente {self.ui_widget.cliente_edit.text()}")
        QMessageBox.information(self.ui_widget, "Nueva Venta", "Venta iniciada correctamente.")
    
    def agregar_item_venta(self):
        """Agrega un ítem a la venta actual."""
        QMessageBox.information(self.ui_widget, "Agregar Ítem",
                               "Función para agregar ítem no implementada.")
    
    def finalizar_venta(self):
        """Finaliza la venta actual."""
        QMessageBox.information(self.ui_widget, "Finalizar Venta",
                               "Función para finalizar venta no implementada.")
    
    def cancelar_venta(self):
        """Cancela la venta actual."""
        self.ui_widget.label_6.setText("No hay venta en curso")
        QMessageBox.information(self.ui_widget, "Cancelar Venta",
                               "Venta cancelada correctamente.")
    
    def mostrar_form_agregar_vendedor(self):
        """Muestra el formulario para agregar un nuevo vendedor."""
        QMessageBox.information(self.ui_widget, "Agregar Vendedor",
                               "Función para agregar vendedor no implementada.")
    
    def mostrar_estadisticas_vendedor(self):
        """Muestra estadísticas de ventas del vendedor seleccionado."""
        # Obtener vendedor seleccionado
        selected_items = self.ui_widget.salesman_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.ui_widget, "Error", "Debe seleccionar un vendedor.")
            return
        
        QMessageBox.information(self.ui_widget, "Estadísticas",
                               "Función para mostrar estadísticas no implementada.")
    
    def calcular_comisiones(self):
        """Calcula las comisiones de los vendedores."""
        mes = self.ui_widget.month_comboBox.currentData()
        anio = self.ui_widget.year_comboBox.currentData()
        
        QMessageBox.information(self.ui_widget, "Comisiones",
                               f"Comisiones para {self.ui_widget.month_comboBox.currentText()} de {anio} calculadas.")