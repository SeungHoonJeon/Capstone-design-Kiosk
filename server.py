from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)

#세션 저장
app.secret_key = "session_cookie"

#데이터베이스 초기 설정
def inital_DB():
    conn = sqlite3.connect('user_test1.db',check_same_thread=False,isolation_level=None)
    c = conn.cursor()
    '''    
    c.execute("CREATE TABLE IF NOT EXISTS table1\
        (id integer primary key AUTOINCREMENT,\
        menu text, price integer, category text, img_path text, real_img_path text, date text)")
    
    c.execute("CREATE TABLE IF NOT EXISTS table2\
        (order_id integer primary key AUTOINCREMENT,\
        order_food text, inquery text, total integer, order_pc, date text)")

    c.execute("CREATE TABLE IF NOT EXISTS table3\
        (idx integer primary key AUTOINCREMENT,\
        name text, id text, password text, join_date text)")
    '''
    return c

#음식 주문 api
def order_food():
    cursor.execute(f"SELECT * FROM table2")
    rows = cursor.fetchall()
    count = len(rows)
    if count < 8:
        empty = 8 - count
        for i in range(empty):
            rows.append(('','','',0,''))
    return rows

def menu():
    cursor.execute("SELECT * FROM table1")
    rows = cursor.fetchall()
    return rows

#주문 음식 api
@app.route("/api/order_food")
def api_order_food():
    rows = order_food()
    return rows

#원격 관리 페이지
@app.route("/remote")
def remote():
    return render_template("./remote.html")

#로그인
@app.route("/login")
def login():
    return render_template("./login.html")

#로그인 api
@app.route("/api/login", methods=['POST'])
def api_login():
    if request.method == "POST":
        id = request.form['id']
        pw = request.form['password']

        print(id,pw)
        cursor.execute(f"SELECT * FROM table3 where id='{id}' and password='{pw}'")
        rows = cursor.fetchall()
        if rows:
            session['id'] = id
            flash("로그인을 성공하였습니다.")
            return "<script>alert('로그인을 성공하였습니다.');location.href='../';</script>"
        else:
            flash("로그인을 실패하였습니다.")
            return "<script>alert('아이디 혹은 패스워드가 일치하지 않습니다.');location.href='../login';</script>"
        
    else:
        return render_template("./login.html")

def delete_menu(idx):
    sql = f"delete from table1 where id={idx}"
    cursor.execute(sql)
    return cursor.rowcount

#처음 페이지
@app.route("/", methods=['GET','POST'])
def hello(username=None, rows=None):
    if 'id' in session:
        if request.method == "GET":
            if request.args.get('id'): #삭제
                idx = request.args.get('id')
                delete_result = delete_menu(idx)
                if delete_result == 1:
                    print("메뉴를 정상적으로 삭제했습니다.")
                    return "<script>alert('메뉴를 정상적으로 삭제했습니다.');location.href='./';</script>"
                else:
                    print("비정상적인 요청으로 삭제하지 못했습니다.")
                    return "<script>alert('메뉴를 정상적으로 삭제했습니다.');location.href='./';</script>"
            else:
                username = session['id']
                rows = order_food() #주문 메뉴 조회
                total_price = sum([rows[i][3] for i in range(len(rows))])
                rows1 = menu() #등록 메뉴 조회
                print(rows)
                print(rows1)
                return render_template("./counter_main.html", username=username, rows = rows, rows1=rows1, total_price=total_price)
        if request.method == "POST":
            action = request.form['action']
            food_name = request.form['food_name']
            food_img = request.files['food_img']
            food_img.save(f"/tmp/{food_img.filename}")
            price = request.form['price']
            category = request.form['category']
            if action == "modifiy":
                pass
                #cursor.execute(f"update table1 set menu={}, price={}, category={}, img_path={}, real_img_path={}, date={} where food_name={} where id={}")
                #return "<script>location.href='./manage';</script>"
            elif action == "add":
                print(action) 
                print(food_name)
                print(food_img)
                print(price)
                print(category)
                cursor.execute(f"insert into table1(menu, price, category, img_path, real_img_path, date) values('{food_name}',{price},'{category}','{food_img.filename}','/tmp/upload/{food_img.filename}','23-04-04')")
                return "<script>alert('메뉴 추가완료');location.href='./';</script>"
    else:
        return "<script>alert('로그인 후 이용해주세요.');location.href='./login'</script>"

if __name__ == "__main__":
    cursor = inital_DB()
    app.run(host='192.168.0.42',port=5050,debug=True)