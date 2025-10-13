class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio
        self.__cantidad = cantidad
    def __str__(self):
        return f"Código: {self.__codigo} - Nombre: {self.__nombre} - Precio: {self.__precio} - Stock: {self.__stock}"
    @property
    def codigo(self):
        return self.__codigo
    @property
    def nombre(self):
        return self.__nombre
    @property
    def precio(self):
        return self.__precio
    @property
    def cantidad(self):
        return self.__cantidad
    
    def __str__(self):
        return f"Código: {self.__codigo:<10}, Nombre: {self.__nombre:<35}, Precio: {self.__precio:>8.2f}, stock: {self.__cantidad:>5}"