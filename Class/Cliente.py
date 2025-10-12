import re

class LongitudDNIInvalido(Exception):
    pass

class LongitudTelefonoInvalido(Exception):
    pass

class FormatoCorreoInvalido(Exception):
    pass

class Cliente():
    def __init__(self, DNI, nombre, correo, teléfono):
        if not isinstance(DNI, str) or len(DNI) != 8 or not DNI.isdigit():
            raise LongitudDNIInvalido(f"El DNI '{DNI}' debe tener exactamente 8 dígitos numéricos.")
        if not isinstance(teléfono, str) or len(teléfono) != 9 or not teléfono.isdigit():
            raise LongitudTelefonoInvalido(f"El teléfono '{teléfono}' debe tener exactamente 9 dígitos numéricos.")
        if not Cliente.validar_correo(correo):
            raise FormatoCorreoInvalido(f"El correo '{correo}' no tiene un formato válido.")
        self.__DNI = DNI
        self.__nombre = nombre
        self.__correo = correo
        self.__teléfono = teléfono

    @staticmethod
    def validar_correo(correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, correo) is not None
    
    def __str__(self):
        return f"DNI: {self.__DNI} - Nombre: {self.__nombre} - Correo: {self.__correo} - Teléfono: {self.__teléfono}"
    
    def get_dni(self):
        return self.__DNI
    
class Tiendita:
    def __init__(self):
        self.__reporte_clientes = []
    
    def registrar_cliente(self, cliente):
        for cli in self.__reporte_clientes:
            if cli.get_dni() == cliente.get_dni():
                raise Exception(f"El cliente {cli.get_dni()} ya esta registrado")
        self.__reporte_clientes.append(cliente)
    def imprimir_reporte (self):
        for cliente in self.__reporte_clientes:
            print(cliente)
            
    def consultar_cliente_por_dni(self, dni):
        for cliente in self.__reporte_clientes:
            if cliente.get_dni() == dni:
                return cliente
        return None


def mostrar_menu():
    print("\n--- GESTIÓN DE CLIENTES ---")
    print("1. Registrar cliente")
    print("2. Reporte de clientes")
    print("3. Consultar cliente por DNI")
    print("4. Salir")
    return input("Seleccione una opción: ")

def registrar_cliente_interactivo(tienda):
    print("\n--- REGISTRO DE CLIENTE ---")
    dni = input("Ingrese DNI: ")
    nombre = input("Ingrese nombre: ")
    correo = input("Ingrese correo: ")
    telefono = input("Ingrese teléfono: ")
    try:
        cliente = Cliente(dni, nombre, correo, telefono)
        tienda.registrar_cliente(cliente)
        print("Cliente registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar cliente: {e}")

def consultar_cliente_interactivo(tienda):
    print("\n--- CONSULTA DE CLIENTE POR DNI ---")
    dni = input("Ingrese el DNI del cliente: ")
    cliente = tienda.consultar_cliente_por_dni(dni)
    if cliente:
        print(f"Cliente encontrado:")
        print(cliente)
    else:
        print("No se encontró un cliente con ese DNI.")

def main():
    tienda = Tiendita()
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            registrar_cliente_interactivo(tienda)
        elif opcion == "2":
            print("\n--- REPORTE DE CLIENTES ---")
            tienda.imprimir_reporte()
        elif opcion == "3":
            consultar_cliente_interactivo(tienda)
        elif opcion == "4":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()