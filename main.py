from Class.Usuario import Admin, Vendedor
import sqlite3

def main():
    print("Bienvenido a la aplicacion")
    print("ingrese su usuario y contraseña")
    conn=sqlite3.connect('Data/Stock.db')
    c=conn.cursor()
    while True:
        usuario=input("Usuario: ")
        contraseña=input("Contraseña: ")
        c.execute("SELECT * FROM Usuarios WHERE Usuario=? AND Contraseña=?", (usuario, contraseña))
        resultado=c.fetchone()
        if resultado:
            print(f"Bienvenido {resultado[0]} {resultado[1]} - Puesto: {resultado[4]}")
            if resultado[4]=="Admin":
                admin=Admin(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
                admin.menuAdmin()
            elif resultado[4]=="Vendedor":
                vendedor=Vendedor(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
                vendedor.menuVendedor()
            else:
                print("Puesto no reconocido.")
            break
        else:
            print("Usuario o contraseña incorrectos. Intente de nuevo.")

if __name__ == "__main__":
    main()
    