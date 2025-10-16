import sqlite3

conn = sqlite3.connect('Data/Stock.db')
c = conn.cursor()

c.execute("DELETE FROM ListComprobantes")
conn.commit()
conn.close()