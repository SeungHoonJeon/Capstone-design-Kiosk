import sqlite3

conn = sqlite3.connect("user_test1.db", isolation_level=None)
c = conn.cursor()

c.execute("delete from table2 where order_id=26")