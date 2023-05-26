import sqlite3

conn = sqlite3.connect("user_test1.db", isolation_level=None)
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' UNION ALL SELECT name FROM sqlite_temp_master WHERE type IN ('table', 'view') ORDER BY 1;")
print(c.fetchall())

c.execute("SELECT * FROM table1;")
print(c.fetchall())
c.execute("SELECT * FROM table2;")
print(c.fetchall())
c.execute("SELECT * FROM table3;")
print(c.fetchall())