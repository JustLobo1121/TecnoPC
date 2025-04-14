import os, json

class Model:
    def __init__(self):
        self._filepath = os.path.join("json", "data.json")
        if not self.check_file():
            try:
                with open(self._filepath, 'r') as data:
                    json.dump({"isNew": 0},self._filepath, indent=4)
                    print(f"has been create the: '{self._filepath}")
            except Exception as e:
                print(f"is not posible to create the json: {e}")

    def check_file(self):
        try:
            if os.path.exists(self._filepath):
                return True  
        except json.JSONDecodeError:
            print(f"Error: the './{self._filepath}' is not a json validate.")
        except Exception as e:
            print(f"Error: is not reading the './{self._filepath}': {e}.")
    def get_data(self):
        try:
            with open(self._filepath, "r") as data_json:
                data = json.load(data_json)
            return data
        except Exception as e:
            raise f"something happend: {e}"
    # modificacion necesaria y terminar conexion con el view pasando el viewmodel:
    # componente
    def actualizar_stock(self, cantidad):
        """
        Actualiza el stock del componente.
        
        Args:
            cantidad (int): Cantidad a añadir (positivo) o quitar (negativo) del stock
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        nuevo_stock = self.stock + cantidad
        if nuevo_stock >= 0:
            self.stock = nuevo_stock
            return True
        return False
    
    def obtener_info_completa(self):
        """
        Retorna la información completa del componente.
        
        Returns:
            dict: Diccionario con todos los atributos del componente
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "marca": self.marca,
            "precio": self.precio,
            "stock": self.stock,
            "descripcion": self.descripcion
        }
    # ---
    # vendedor
    def registrar_venta(self, venta: list):
        """
        Registra una nueva venta realizada por el vendedor.
        
        Args:
            venta (Venta): Objeto venta a registrar
            
        Returns:
            bool: True si se registró correctamente
        """
        self.ventas.append(venta)
        return True
    
    def calcular_comisiones(self, mes, anio):
        """
        Calcula las comisiones del vendedor en un período específico.
        
        Args:
            mes (int): Mes para calcular comisiones
            anio (int): Año para calcular comisiones
            
        Returns:
            float: Total de comisiones del período
        """
        total_ventas = 0
        for venta in self.ventas:
            if venta.mes == mes and venta.anio == anio:
                total_ventas += venta.total
        
        # Comisión del 5% sobre el total de ventas
        return total_ventas * 0.05
    
    def obtener_info_vendedor(self):
        """
        Retorna la información del vendedor.
        
        Returns:
            dict: Diccionario con los datos del vendedor
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "tienda": self.tienda.nombre if self.tienda else None,
            "fecha_contratacion": self.fecha_contratacion
        }
    # ---
    # tienda
    def agregar_vendedor(self, vendedor):
        """
        Agrega un vendedor a la tienda.
        
        Args:
            vendedor (Vendedor): Vendedor a agregar
            
        Returns:
            bool: True si se agregó correctamente
        """
        if vendedor not in self.vendedores:
            self.vendedores.append(vendedor)
            vendedor.tienda = self
            return True
        return False
    
    def agregar_componente(self, componente, cantidad=1):
        """
        Agrega un componente al inventario de la tienda.
        
        Args:
            componente (Componente): Componente a agregar
            cantidad (int, optional): Cantidad a agregar. Default es 1.
            
        Returns:
            bool: True si se agregó correctamente
        """
        if componente.id in self.inventario:
            self.inventario[componente.id]["cantidad"] += cantidad
        else:
            self.inventario[componente.id] = {
                "componente": componente,
                "cantidad": cantidad
            }
        return True
    
    def buscar_componente(self, id_componente):
        """
        Busca un componente en el inventario de la tienda.
        
        Args:
            id_componente (int): ID del componente a buscar
            
        Returns:
            dict: Información del componente si existe, None en caso contrario
        """
        if id_componente in self.inventario:
            return self.inventario[id_componente]
        return None
    
    def listar_componentes_por_tipo(self, tipo):
        """
        Lista todos los componentes de un tipo específico.
        
        Args:
            tipo (str): Tipo de componente a buscar (RAM, Procesador, etc.)
            
        Returns:
            list: Lista de componentes del tipo especificado
        """
        componentes = []
        for item in self.inventario.values():
            if item["componente"].tipo == tipo:
                componentes.append({
                    "componente": item["componente"],
                    "cantidad": item["cantidad"]
                })
        return componentes
    
    def obtener_info_tienda(self):
        """
        Retorna la información de la tienda.
        
        Returns:
            dict: Diccionario con los datos de la tienda
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "telefono": self.telefono,
            "email": self.email,
            "horario": f"{self.horario_apertura} - {self.horario_cierre}",
            "vendedores": len(self.vendedores),
            "componentes_distintos": len(self.inventario)
        }