import sqlite3
db = sqlite3.connect('power.db')

c = db.cursor()

c.execute("""CREATE TABLE pressure(name text, age text, normal pressure integer, pressure_of_pepople integer)""")

db.commit()
db.close()