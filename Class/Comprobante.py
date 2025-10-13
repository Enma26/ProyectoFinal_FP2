def generar_numero_comprobante(tipo):
    import sqlite3
    conn = sqlite3.connect('Data/Stock.db')
    c = conn.cursor()
    c.execute("Select serie_numero from Comprobantes where tipo=?", (tipo,))
    fila = c.fetchone()
    if fila:
        serie,numero = fila[0].split('-')
        numero=int(numero)+1
    else:
        serie = "B001" if tipo == "Boleta" else "F001"
        numero = 1
    conn.close()
    return f"{serie}-{numero:06d}"

class Comprobante:
    IGV = 0.18 

    def __init__(self, numero, cliente, productos, tipo):
        self.__numero = numero
        self.__cliente = cliente
        self.__productos = productos
        self.__tipo = tipo
    
    def __Calcular_subtotal(self):
        subtotal = sum(p.precio * p.cantidad for p in self.__productos)
        return subtotal
    
    def __Calcular_igv(self):
        if self.__tipo == "Factura":
            return self.__Calcular_subtotal() * self.IGV
        return 0.0
    def __Calcular_total(self):
        return self.__Calcular_subtotal() + self.__Calcular_igv()
    
    def Imprimir_Comprobante(self):
        print(f"--- {self.__tipo} ---")
        print(f"Número: {self.__numero}")
        print(f"Cliente: {self.__cliente.nombre} {self.__cliente.apellido} - DNI: {self.__cliente.DNI}")
        print("Productos:")
        for p in self.__productos:
            print(f"{p.codigo} - {p.nombre} (x{p.cantidad}): ${p.precio * p.cantidad:.2f}")
        print(f"Subtotal: ${self.__Calcular_subtotal():.2f}")
        print(f"IGV: ${self.__Calcular_igv():.2f}")
        print(f"Total: ${self.__Calcular_total():.2f}")
        print("gracias por su compra!")
        print("-------------------")
    
class Boleta(Comprobante):
    def __init__(self, cliente, productos):
        numero = generar_numero_comprobante("Boleta")
        super().__init__(numero, cliente, productos, "Boleta")

class Factura(Comprobante):
    def __init__(self, cliente, productos):
        numero = generar_numero_comprobante("Factura")
        super().__init__(numero, cliente, productos, "Factura")
