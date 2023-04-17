import sqlite3

conn = sqlite3.connect("user_test1.db", isolation_level=None)
c = conn.cursor()

print(c)

#id	메뉴 이름	가격	카테고리	사진 경로 원본	저장 위치	등록일자
#id,menu, price, category, img_path, real_img_path, date
c.execute("CREATE TABLE IF NOT EXISTS table1\
    (id integer primary key AUTOINCREMENT,\
    menu text, price integer, category text, img_path text, real_img_path text, date text)")

#id	주문번호	주문음식	요청사항	 총 결제 금액	 주문 일자
#id,order_id, order_food, inquery, total, date
c.execute("CREATE TABLE IF NOT EXISTS table2\
    (order_id integer primary key AUTOINCREMENT,\
    order_food text, inquery text, total integer, order_pc text, date text)")

#idx	id	password	가입일
#id, name, password, join_date
c.execute("CREATE TABLE IF NOT EXISTS table3\
    (idx integer primary key AUTOINCREMENT,\
    name text, id text, password text, join_date text)")

c.execute("insert into table1(menu, price, category, img_path, real_img_path, date) values('햄버거',3000,'주메뉴','/tmp','/tmp/upload','23-04-04')")
c.execute("insert into table2(order_food, inquery, total, order_pc, date) values('햄버거(1),콜라(1)','토마토 뺴주세요','10000','192.168.0.15','23-04-06') ")
c.execute("insert into table3(name, id, password, join_date) values('admin','admin','admin','23-04-06')")

c.execute("SELECT * FROM table1")
print(c.fetchone())
c.execute("SELECT * FROM table2")
print(c.fetchone())
c.execute("SELECT * FROM table3")
print(c.fetchone())



