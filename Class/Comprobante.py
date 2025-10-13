class Comprobante:
  
  IGV_RATE = 0.18 

  def __init__(self, tipo, numero, cliente, vendedor, items):
    self._tipo = tipo.upper()          
    self._numero = numero              
    self._cliente = cliente            
    self._vendedor = vendedor          
    self._items = items                

#calcula subtotal, igv y total
  def calcular_subtotal(self):
    return sum(prod._precio * cant for prod, cant in self._items)

  def calcular_igv(self):
    return self.calcular_subtotal() * Comprobante.IGV_RATE

  def calcular_total(self):
    return self.calcular_subtotal() + self.calcular_igv()

  def generar_comprobante(self):

# Genera el texto del comprobante.
    texto = f"\n{'='*45}\n"
    texto += f"          COMPROBANTE DE VENTA ({self._tipo})\n"
    texto += f"{'='*45}\n"
    texto += f"N°: {self._numero}\nFecha: {self._fecha}\n"
    texto += f"Cliente: {self._cliente}\nVendedor: {self._vendedor}\n"
    texto += f"{'-'*45}\n"
    texto += f"{'Producto':20} {'Cant.':>6} {'P.Unit':>10} {'Subtotal':>10}\n"
    texto += f"{'-'*45}\n"

    for prod, cant in self._items:
      subtotal = prod._precio * cant
      texto += f"{prod._nombre:20} {cant:>6} {prod._precio:>10.2f} {subtotal:>10.2f}\n"

    texto += f"{'-'*45}\n"
    texto += f"Subtotal:{self.calcular_subtotal():>33.2f}\n"
    texto += f"IGV (18%):{self.calcular_igv():>32.2f}\n"
    texto += f"TOTAL:{self.calcular_total():>36.2f}\n"
    texto += f"{'='*45}\n"
    return texto

  def __str__(self):
    return f"{self._tipo} N° {self._numero} - Cliente: {self._cliente} - Total: S/ {self.calcular_total():.2f}"


class Boleta(Comprobante):
  def __init__(self, numero, cliente, vendedor, items):
    super().__init__("BOLETA", numero, cliente, vendedor, items)

  def generar_comprobante(self):
 
# Personaliza el formato de Boleta.
    texto = super().generar_comprobante()
    texto += "Gracias por su compra. ¡Vuelva pronto!\n"
    return texto


class Factura(Comprobante):
  def __init__(self, numero, cliente, vendedor, items, ruc_cliente):
    super().__init__("FACTURA", numero, cliente, vendedor, items)
    self._ruc_cliente = ruc_cliente

  def generar_comprobante(self):

# Personaliza el formato de Factura.
    texto = super().generar_comprobante()
    texto += f"RUC Cliente: {self._ruc_cliente}\n"
    texto += "Documento válido para crédito fiscal.\n"
    return texto

# cambialo para el main, lo vi en cliente.py
class Tiendita:
  def __init__(self):
    self._comprobantes = []
    self._correlativos = {"BOLETA": 0, "FACTURA": 0}

  def _siguiente_correlativo(self, tipo):
    self._correlativos[tipo] += 1
    return f"{self._correlativos[tipo]:06d}"

  def generar_comprobante(self, tipo, cliente, vendedor, items, ruc_cliente=None):
    """Genera y registra un comprobante según su tipo."""
    numero = self._siguiente_correlativo(tipo.upper())

    if tipo.upper() == "BOLETA":
      comprobante = Boleta(numero, cliente, vendedor, items)
    elif tipo.upper() == "FACTURA":
      comprobante = Factura(numero, cliente, vendedor, items, ruc_cliente)
    else:
      raise ValueError("Tipo de comprobante no válido. Use 'BOLETA' o 'FACTURA'.")

    self._comprobantes.append(comprobante)
    return comprobante


# prueba de ejecución (main)
def main():
  class Producto:
    def __init__(self, nombre, precio):
      self._nombre = nombre
      self._precio = precio

  # Productos simulados
  prod1 = Producto("Mouse", 50)
  prod2 = Producto("Teclado", 120)

  # Crear tiendita
  tienda = Tiendita()

  # Generar Boleta
  boleta = tienda.generar_comprobante("BOLETA", "Juan Pérez", "Vendedor 1", [(prod1, 2), (prod2, 1)])
  print(boleta.generar_comprobante())

  # Generar Factura
  factura = tienda.generar_comprobante("FACTURA", "Empresa XYZ", "Vendedor 2", [(prod2, 5)], "20123456789")
  print(factura.generar_comprobante())


if __name__ == "__main__":
  main()
