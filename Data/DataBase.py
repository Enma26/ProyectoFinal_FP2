import sqlite3

conn = sqlite3.connect('Data/Stock.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE Usuarios RENAME TO Usuarios_old;")
    c.execute("""
              CREATE TABLE Usuarios (
              Nombre TEXT,
              Apellido TEXT,
              Usuario TEXT PRIMARY KEY,
              Contraseña TEXT,
              Puesto TEXT
              );
              """)
    c.execute("""
              INSERT INTO Usuarios (Nombre, Apellido, Usuario, Contraseña, Puesto)
              SELECT Nombre, Apellido, Usuario, Contraseña, Puesto FROM Usuarios_old;
              """)
    c.execute("DROP TABLE Usuarios_old;")
    conn.commit()
except sqlite3.Error as e:
    print(f"Error al actualizar la base de datos: {e}")
    conn.rollback()
finally:
    conn.close()