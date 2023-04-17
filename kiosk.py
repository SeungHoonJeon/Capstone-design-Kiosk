from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)


@app.route("/remote", method=["GET","POST"])
def remote():
    if request.method == "GET":
        return render_template("remote.html")
    else:
        pass

if __name__ == "__main__":
    app.run(host='192.168.66.128',port=5051,debug=True)