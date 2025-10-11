import sqlite3

class Usuario:
    def __init__(self, nombre, apellido, usuario, contraseña, puesto):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__usuario = usuario
        self.__contraseña = contraseña
        self.__puesto = puesto
    
    def RegistrarCliente(self):
        pass

    def RegistrarVenta(self):
        pass
    
    def __str__(self):
        return f"Nombre: {self.__nombre}, Apellido: {self.__apellido}, Usuario: {self.__usuario}, Puesto: {self.__puesto}"

class Admin(Usuario):
    def __init__(self, nombre, apellido, usuario, contraseña, puesto):
        super().__init__(nombre, apellido, usuario, contraseña, puesto)
        
    def CrearUsuario(self):
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        usuario = nombre.lower()[0] + apellido.lower()[0:4]
        contraseña = input("Ingrese la contraseña: ")
        puesto = input("Ingrese el puesto (Admin/Vendedor): ")
        
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        c.execute("INSERT INTO Usuarios (Nombre, Apellido, Usuario, Contraseña, Puesto) VALUES (?, ?, ?, ?, ?)", 
                  (nombre, apellido, usuario, contraseña, puesto))
        conn.commit()
        conn.close()
        print(f"Usuario {usuario} creado exitosamente.")
    
    def RegistrarProducto(self):
        pass

    def menuAdmin(self):
        while True:
            print("1. Crear Usuario")
            print("2. Registrar Producto")
            print("3. Salir")
            try:
                opcion = int(input("Seleccione una opcion: "))
                if opcion == 1:
                    self.CrearUsuario()
                elif opcion == 2:
                    self.RegistrarProducto()
                elif opcion == 3:
                    print("Saliendo...")
                    break
                else:
                    print("Opcion no valida.")
            except ValueError:
                print("Por favor ingrese un numero valido.")
    
class Vendedor(Usuario):
    def __init__(self, nombre, apellido, usuario, contraseña, puesto):
        super().__init__(nombre, apellido, usuario, contraseña, puesto)
    
    def MenuVendedor(self):
        while True:
            print("1. Registrar Cliente")
            print("2. Registrar Venta")
            print("3. Salir")
            try:
                opcion = int(input("Seleccione una opcion: "))
                if opcion == 1:
                    self.RegistrarCliente()
                elif opcion == 2:
                    self.RegistrarVenta()
                elif opcion == 3:
                    print("Saliendo...")
                    break
                else:
                    print("Opcion no valida.")
            except ValueError:
                print("Por favor ingrese un numero valido.")
