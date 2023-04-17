from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)

#세션 저장
app.secret_key = "session_cookie"

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

def order_food():
    cursor.execute(f"SELECT * FROM table2")
    rows = cursor.fetchall()
    return rows

@app.route("/api/order_food")
def api_order_food():
    rows = order_food()
    return f"{rows}"

@app.route("/")
def hello(username=None, rows=None):
    if 'id' in session:
        username = session['id']
        rows = order_food()
        return render_template("./counter_main.html", username=username, rows = rows)
    else:
        return render_template("./index.html")

@app.route("/manage", methods=['POST','GET'])
def manage(rows=None, item=None):
    if request.method == "GET":
        cursor.execute("SELECT * FROM table1")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM table2")
        items = cursor.fetchall()
        sum = 0
        for item in items:    
            print(item)
            sum += item[3]
        return render_template("./manage.html", rows=rows, sum=sum)
    if request.method == "POST":
        operation = request.form['operation']
        food_name = request.form['food_name']
        food_img = request.files['food_img']
        food_img.save(f"/tmp/{food_img.filename}")
        price = request.form['price']
        category = request.form['category']
        
        print(operation) 
        print(food_name)
        print(food_img)
        print(price)
        print(category)

        if operation == '1':
            cursor.execute(f"insert into table1(menu, price, category, img_path, real_img_path, date) values('{food_name}',{price},'{category}','{food_img.filename}','/tmp/upload/{food_img.filename}','23-04-04')")
            return "<script>location.href='./manage';</script>"
        elif operation == '2':
            #수정
            pass
            #cursor.execute(f"update table1 set menu={}, price={}, category={}, img_path={}, real_img_path={}, date={} where food_name={} where id={}")
        else:
            #삭제
            pass
@app.route("/login")
def login():
    return render_template("./login.html")

@app.route("/remote")
def remote():
    return render_template("./remote.html")


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
   
if __name__ == "__main__":
    cursor = inital_DB()
    app.run(host='192.168.66.128',port=5050,debug=True)