from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, render_template_string
import sqlite3, os, json
from datetime import datetime

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
    sql = f"select * from table1 where id={idx}"
    cursor.execute(sql)
    rows = cursor.fetchone()
    print(rows)
    os.remove(rows[5])
    sql = f"delete from table1 where id={idx}"
    cursor.execute(sql)
    return cursor.rowcount

@app.route("/kiosk", methods=['GET','POST'])
def kiosk():
    rows = menu() #음식 조회
    print(rows)
    return render_template("./kiosk_client.html", rows=rows)

@app.route("/kiosk/order", methods=['POST'])
def order():
    data = request.get_json()
    print(data)
    s = []
    for item in data:
        if 'name' in item and 'quantity' in item:
            s.append(item['name'])
            s.append(item['quantity'])
        if 'inputrequest' in item and 'totalPrice' in item:
            s.append(item['totalPrice'])
            s.append(item['inputrequest'])
    print(s)
    food_total_string = ' '.join([f'{s[i]}x{s[i+1]}' for i in range(0, len(s[0:-2]), 2)])
    totalPrice = s[len(s)-2]
    inputrequest = s[len(s)-1]
    data_to_dict = {
        "food_total_string" : food_total_string,
        "totalPrice" : totalPrice,
        "inputrequest" : inputrequest
    }     
    return jsonify(data_to_dict)

def complte_order(data):
    now = datetime.now()
    print(data)
    for i in data:
        order_food = i['food_total_string']
        order_request = i['inputrequest']
        order_totalprice = i['totalPrice']
    ip_address = request.remote_addr
    try:
        cursor.execute(f"insert into table2(order_food, inquery, total, order_pc, date) values('{order_food}','{order_request}','{order_totalprice}','{ip_address}','{now.strftime('%Y-%m-%d %H:%M:%S')}')")
        html = f"""
            { order_food }
            { order_totalprice }
            { order_request }
        """
        return html
    except Exception as e:
        print("에러 발생:", e)
        return 0


@app.route("/kiosk/payment", methods=['POST'])
def payment():
    data = request.get_json()

    ### 카드 결제 ###



    #################
    result = complte_order(data)

    if result == -1:
        return "주문실패"
    else:
        ### 영수증 출력 ###


        ##################
        return render_template_string(result)


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
            now = datetime.now()
            action = request.form['action']
            food_name = request.form['food_name']
            food_img = request.files['food_img']
            if food_img.filename == '':
                print(food_img.filename)
            else:
                print('1',food_img.filename)
                food_img.save(f"./static/food/{food_img.filename}")
            price = request.form['price']
            category = request.form['category']
            if action == "modify":
                id = request.form['id']
                if food_img.filename == '':
                    cursor.execute(f"update table1 set menu='{food_name}', price={price}, category='{category}', date='{now.strftime('%Y-%m-%d %H:%M:%S')}' where id={id}")
                else:    
                    cursor.execute(f"update table1 set menu='{food_name}', price={price}, category='{category}', img_path='{food_img.filename}', real_img_path='./static/food/{food_img.filename}', date='{now.strftime('%Y-%m-%d %H:%M:%S')}' where id={id}")
                return "<script>location.href='./';</script>"
            elif action == "add":
                print(action) 
                print(food_name)
                print(food_img)
                print(price)
                print(category)
                cursor.execute(f"insert into table1(menu, price, category, img_path, real_img_path, date) values('{food_name}',{price},'{category}','{food_img.filename}','./static/food/{food_img.filename}','{now.strftime('%Y-%m-%d %H:%M:%S')}')")
                return "<script>alert('메뉴 추가완료');location.href='./';</script>"
    else:
        return "<script>alert('로그인 후 이용해주세요.');location.href='./login'</script>"

if __name__ == "__main__":
    cursor = inital_DB()
    app.run(host='192.168.66.128',port=5050,debug=True)