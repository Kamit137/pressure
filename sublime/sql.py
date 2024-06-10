import sqlite3
db = sqlite3.connect('power.db')

c = db.cursor()

#c.execute("""CREATE TABLE art(title text, full_text text, viw integer)""")

db.commit()
db.close()