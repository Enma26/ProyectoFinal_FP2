import sqlite3

conn=sqlite3.connect('Data/Stock.db')
c=conn.cursor()


c.execute("ALTER TABLE comprobantes RENAME TO ListComprobantes")


conn.commit
conn.close()

