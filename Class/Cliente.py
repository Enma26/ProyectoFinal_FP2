class Cliente:
    def __init__(self, DNI, nombre, apellido, direccion, telefono):
        self.__DNI = DNI
        self.__nombre = nombre
        self.__apellido = apellido
        self.__direccion = direccion
        self.__telefono = telefono
    
    @property
    def DNI(self):
        return self.__DNI
    @property
    def nombre(self):
        return self.__nombre
    @property
    def apellido(self):
        return self.__apellido
    @property
    def direccion(self):
        return self.__direccion
    @property
    def telefono(self):
        return self.__telefono
    