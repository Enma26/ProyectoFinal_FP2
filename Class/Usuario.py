import re

class Usuario:
    def __init__(self, nombre, apellido, usuario, contraseña, puesto):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__usuario = usuario
        self.__contraseña = contraseña
        self.__puesto = puesto
    def ConsultarCliente(self):
        from Class.Cliente import Cliente
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        while True:
            try:
                dni=input("Ingrese el DNI del cliente: ")
                if dni and not re.match(r"^\d{7,8}$", dni):
                    raise ValueError("DNI inválido. Debe contener solo dígitos y tener 7 u 8 caracteres.")
                c.execute("SELECT * FROM Clientes WHERE DNI=?", (dni,))
                resultado=c.fetchone()
                if resultado:
                    print(f"Bienvenido Sr(a). {resultado[1]} {resultado[2]}")
                    cliente=Cliente(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
                    conn.close()
                    return cliente
                else:
                    nombre=input("Ingrese el nombre del cliente: ")
                    apellido=input("Ingrese el apellido del cliente: ")
                    correo=input("Ingrese el correo del cliente: ")
                    if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
                        raise ValueError("Correo inválido. Debe tener un formato válido.")
                    telefono=input("Ingrese el teléfono del cliente: ")
                    if telefono and not re.match(r"^\+?\d{7,15}$", telefono):
                        raise ValueError("Teléfono inválido. Debe contener solo dígitos y opcionalmente un '+' al inicio.")
                    c.execute("INSERT INTO Clientes (DNI, Nombre, Apellido, Correo, Telefono) VALUES (?, ?, ?, ?, ?)", (dni, nombre, apellido, correo, telefono))
                    conn.commit()
                    print("Cliente registrado exitosamente.")
                    cliente=Cliente(dni, nombre, apellido, correo, telefono)
                    conn.close()
                    return cliente
            except Exception as e:
                print(f"Ocurrió un error: {e}")
    def ListaVenta(self):
        from Class.Producto import Producto
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        listaproductos=[]
        while True:
            try:
                codigo=input("Ingrese el código del producto (o 'listo' para terminar): ")
                if codigo.lower() == 'listo':
                    break
                c.execute("SELECT * FROM Productos WHERE Codigo=?", (codigo,))
                resultado=c.fetchone()
                if resultado:
                    cantidad=int(input("Ingrese la cantidad a comprar: "))
                    if cantidad <= 0:
                        raise ValueError("La cantidad debe ser un número positivo.")
                    if cantidad > resultado[3]:
                        raise ValueError("Cantidad insuficiente en stock.")
                    producto=Producto(resultado[0], resultado[1], resultado[2], cantidad)
                    listaproductos.append(producto)
                else:
                    print("Producto no encontrado. Intente de nuevo.")
            except Exception as e:
                print(f"Ocurrió un error: {e}")
        conn.close()
        return listaproductos
    
    def Iniciar_Venta(self):
        from Class.Comprobante import Boleta, Factura
        print("ingresar datos del cliente")
        cliente=self.ConsultarCliente()
        listaproductos=self.ListaVenta()
        if not listaproductos:
            print("No se seleccionaron productos. Venta cancelada.")
            return
        while True:
            try:
                tipo_comprobante=input("Ingrese el tipo de comprobante (Boleta/Factura): ")
                if tipo_comprobante not in ["Boleta", "Factura", "Salir"]:
                    raise ValueError("Tipo de comprobante inválido. Debe ser 'Boleta', 'Factura' o 'Salir'.")
                elif tipo_comprobante == "Boleta":
                    comprobante=Boleta(cliente, listaproductos)
                    comprobante.Imprimir_Comprobante()
                    for i in listaproductos:
                        import sqlite3
                        conn=sqlite3.connect('Data/Stock.db')
                        c=conn.cursor()
                        c.execute("UPDATE Productos SET Stock = Stock - ? WHERE Codigo=?", (i.cantidad, i.codigo))
                        conn.commit()
                        conn.close()
                    break
                elif tipo_comprobante == "Factura":
                    comprobante=Factura(cliente, listaproductos)
                    comprobante.Imprimir_Comprobante()
                    for i in listaproductos:
                        import sqlite3
                        conn=sqlite3.connect('Data/Stock.db')
                        c=conn.cursor()
                        c.execute("UPDATE Productos SET Stock = Stock - ? WHERE Codigo=?", (i.cantidad, i.codigo))
                        conn.commit()
                        conn.close()
                    break
                elif tipo_comprobante == "Salir":
                    print("Venta cancelada.")
                    break
            except Exception as e:
                print(f"Ocurrió un error: {e}")
    
class Admin(Usuario):
    def __init__(self, nombre, apellido, usuario, contraseña, puesto):
        super().__init__(nombre, apellido, usuario, contraseña, puesto)
    
    def crearUsuario(self):
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        try:
            nombre=input("Ingrese el nombre del nuevo usuario: ")
            apellido=input("Ingrese el apellido del nuevo usuario: ")
            usuario=nombre[0].lower()+apellido[0:5].lower()
            contraseña=input("Ingrese la contraseña: ")
            puesto=input("Ingrese el puesto (Admin/Vendedor): ")
            if puesto not in ["Admin", "Vendedor"]:
                raise ValueError("Puesto inválido. Debe ser 'Admin' o 'Vendedor'.")
            c.execute("INSERT INTO Usuarios (Nombre, Apellido, Usuario, Contraseña, Puesto) VALUES (?, ?, ?, ?, ?)", (nombre, apellido, usuario, contraseña, puesto))
            conn.commit()
            conn.close()
            print("Usuario creado exitosamente.")
        except ValueError as ve:
            print(ve)
    def menuAdmin(self):
        while True:
            print("\n--- Menú Admin ---")
            print("1. Inicio de venta")
            print("2. Crear Usuario")
            print("3. Gestor de Productos")
            print("4. Reporte de Ventas")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.Iniciar_Venta()
            elif opcion == "2":
                self.crearUsuario()
            elif opcion == "3":
                self.menuAlmacen()
            elif opcion == "4":
                self.ReporteVentas()
            elif opcion == "5":
                print("Saliendo del menú Admin.")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
    
    def __ActualizarDisponibilidad(self,codigo_producto):
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        c.execute("SELECT Stock FROM Productos WHERE Codigo=?", (codigo_producto,))
        resultado=c.fetchone()
        if resultado:
            stock=resultado[0]
            disponible=1 if stock > 10 else 0
            c.execute("UPDATE Productos SET Disponible=? WHERE Codigo=?", (disponible, codigo_producto))
            conn.commit()
        conn.close()

    def __ActualizarFechaModificacion(self,codigo_producto):
        import sqlite3
        from datetime import datetime
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        fecha_modificacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("Update Productos SET FechaModificacion=? WHERE Codigo=?", (fecha_modificacion, codigo_producto))
        conn.commit()
        conn.close()

    def ReporteVentas(self):
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        mes = input("Ingrese el mes (AAAA-MM, ej. 2025-10): ").strip()
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", mes):
            print("Formato inválido. Use AAAA-MM.")
            conn.close()
            return
        c.execute("""
            SELECT Serie_Numero, Tipo, Dni_Cliente, Fecha, Total
            FROM ListComprobantes
            WHERE strftime('%Y-%m', Fecha) = ?
            ORDER BY Fecha ASC
        """, (mes,))
        venta=c.fetchall()
        print("Reporte de Ventas")
        print("-"*80)
        total_general=0
        if venta:
            print(f"{'Serie-Numero':<15} | {'Tipo':<12} | {'Dni_Cliente':<12} | {'Fecha':<20} | {'Total':>10}")
            print("-"*80)
            total_general=0.0
            for vent in venta:
                print(f"{vent[0]:<15} | {vent[1]:<12} | {vent[2]:<12} | {vent[3]:<20} | {vent[4]:>10.2f}")
                total_general += vent[4]
            print("-"*80)
            print(f"{'Total General':<15} | {'':<12} | {'':<12} | {'':<20} | {total_general:>10.2f}")
        else:
            print("No se encontraron ventas para el mes especificado.")
        conn.close()

    def menuAlmacen(self):
        while True:
            print("\n--- Menú Gestor de Productos ---")
            print("1. Agregar Producto")
            print("2. Eliminar merma de Productos")
            print("3. Listar Productos")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.AgregarProducto()
            elif opcion == "2":
                self.RestockearProducto()
            elif opcion == "3":
                self.ListarProductos()
            elif opcion == "4":
                print("Saliendo del menú Gestor de Productos.")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
    
    def ListarProductos(self):
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        c.execute("SELECT * FROM Productos")
        productos=c.fetchall()
        if productos:
            print(f"{'Código':<10} {'Nombre':<35} {'Precio':>8} {'Stock':>5}")
            print("-" * 60)
            for producto in productos:
                print(f"{producto[0]:<10} {producto[1]:<35} {producto[2]:>8.2f} {producto[3]:>5}")
        else:
            print("No hay productos en el inventario.")
        conn.close()
    
    def RestockearProducto(self):
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        try:
            codigo=input("Ingrese el código del producto a modificar: ")
            c.execute("SELECT * FROM Productos WHERE Codigo=?", (codigo,))
            producto=c.fetchone()
            if producto:
                cantidad=int(input("Ingrese la cantidad a eliminar: "))
                if cantidad < 0:
                    raise ValueError("La cantidad a eliminar no puede ser negativa.")
                elif cantidad > producto[3]:
                    raise ValueError("No se puede eliminar más de lo que hay en stock.")
                else:
                    c.execute("UPDATE Productos SET Stock = Stock - ? WHERE Codigo=?", (cantidad, codigo))
                    conn.commit()
                    conn.close()
                    self.__ActualizarFechaModificacion(codigo)
                    self.__ActualizarDisponibilidad(codigo)
                    print("Stock actualizado exitosamente.")
            else:
                print("Producto no encontrado.")
        except Exception as ve:
            print(ve)

    def AgregarProducto(self):
        import sqlite3
        conn=sqlite3.connect('Data/Stock.db')
        c=conn.cursor()
        try:
            codigo=input("Ingrese el código del producto: ")
            c.execute("SELECT * FROM Productos WHERE Codigo=?", (codigo,))
            if c.fetchone():
                cantidad=int(input("El producto ya existe. Ingrese la cantidad a agregar al stock: "))
                if cantidad < 0:
                    raise ValueError("La cantidad a agregar no puede ser negativa.")
                c.execute("UPDATE Productos SET Stock = Stock + ? WHERE Codigo=?", (cantidad, codigo))
                conn.commit()
                conn.close()
                self.__ActualizarDisponibilidad(codigo)
                self.__ActualizarFechaModificacion(codigo)
                print("Stock actualizado exitosamente.")
            else:
                nombre=input("Ingrese el nombre del producto: ")
                precio=float(input("Ingrese el precio del producto: "))
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo.")
                cantidad=int(input("Ingrese la cantidad inicial en stock: "))
                if cantidad < 0:
                    raise ValueError("La cantidad en stock no puede ser negativa.")
                c.execute("INSERT INTO Productos (Codigo, Nombre, Precio, Stock) VALUES (?, ?, ?, ?)", (codigo, nombre, precio, cantidad))
                conn.commit()
                conn.close()
                print("Producto agregado exitosamente.")
        except Exception as ve:
            print(ve)

class Vendedor(Usuario):
    def __init__(self, nombre, apellido, usuario, contraseña, puesto):
        super().__init__(nombre, apellido, usuario, contraseña, puesto)

    def menuVendedor(self):
        while True:
            try:
                print("\n--- Menú Vendedor ---")
                print("1. Iniciar Venta")
                print("2. Salir")
                opcion = input("Seleccione una opción: ")
                if opcion == "1":
                    self.Iniciar_Venta()
                elif opcion == "2":
                    print("Saliendo del menú Vendedor.")
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
            except Exception as e:
                print(f"Ocurrió un error: {e}")
    
    




        