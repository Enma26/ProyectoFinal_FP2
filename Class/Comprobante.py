def generar_numero_comprobante(tipo):
    import sqlite3
    serie = "B001" if tipo == "Boleta" else "F001"
    conn = sqlite3.connect('Data/Stock.db')
    c = conn.cursor()
    c.execute("""
        SELECT Serie_Numero
        FROM ListComprobantes
        WHERE Tipo = ? AND Serie_Numero LIKE ?
        ORDER BY Serie_Numero DESC
        LIMIT 1
    """, (tipo, f"{serie}-%"))
    fila = c.fetchone()
    if fila:
        ultimo_numero = fila[0]
        try:
            numero=int(ultimo_numero.split('-')[1])+1
        except Exception:
            numero=1
    else:
        numero = 1
    
    while True:
        candidato = f"{serie}-{numero:06d}"
        c.execute("SELECT 1 FROM ListComprobantes WHERE Serie_Numero = ?", (candidato,))
        if not c.fetchone():
            conn.close()
            return candidato
        numero += 1


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
        from Class.Cliente import Cliente
        import datetime
        import sqlite3
        conn = sqlite3.connect('Data/Stock.db')
        c = conn.cursor()
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
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO ListComprobantes (Serie_Numero, Tipo, Dni_Cliente, Fecha, Total) VALUES (?, ?, ?, ?, ?)", 
                  (self.__numero,self.__tipo, self.__cliente.DNI, fecha, self.__Calcular_total()))
        conn.commit()
        conn.close()


    
class Boleta(Comprobante):
    def __init__(self, cliente, productos):
        numero = generar_numero_comprobante("Boleta")
        super().__init__(numero, cliente, productos, "Boleta")

class Factura(Comprobante):
    def __init__(self, cliente, productos):
        numero = generar_numero_comprobante("Factura")
        super().__init__(numero, cliente, productos, "Factura")
