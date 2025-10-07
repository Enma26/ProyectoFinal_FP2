import sqlite3

conn = sqlite3.connect('DataBase/Stock.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Usuarios(
          Nombre TEXT,
          Apellido TEXT,
          Puesto TEXT,
          Usuario TEXT PRIMARY KEY,
          Contraseña TEXT)""")
c.execute("INSERT OR IGNORE INTO Usuarios VALUES ('Admin', 'Admin', 'Admin', 'admin', 'admin123')")

conn.commit()
conn.close()