from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = 'jerson'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    salt = 'esmael'
    p = (request.form['password']+salt).encode()
    conn = sqlite3.connect('auditoria.db')
    #password = generate_password_hash(request.form['password'])
    cursor = conn.execute("SELECT * from UTILIZADOR where \
                USER = '"+ request.form['user'] + "' and PASSWORD = '"+ hashlib.sha512(p).hexdigest() + "'")

    result = 0
    for row in cursor:
        userID = row[0]
        userTYPE = row[3]
        result = result + 1
    if result == 1:
        session['user'] = userID
        if userTYPE == 'admin':
            conn.close()
            return redirect(url_for('mainpageAdmin'))
        else:
            conn.close()
            return redirect(url_for('mainpage'))
    else:
        conn.close()
        return index()


@app.route('/mainpage')
def mainpage():
    if 'user' in session:
        if session['user'] != 1:
            return render_template('mainpage.html')
        else:
            return render_template('permition.html')
    else:
        return render_template('login.html')

@app.route('/mainpageAdmin')
def mainpageAdmin():
    if 'user' in session:
        if session['user'] == 1:
            conn = sqlite3.connect('auditoria.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * from UTILIZADOR ")
            rows = cursor.fetchall()
            conn.close()
            return render_template('mainpageAdmin.html', rows = rows)
        else:
            return render_template('permition.html')
    else:
        return render_template('login.html')

@app.route('/mainpageAdmin/updateUser')
def updateUser():
    if 'user' in session:
        if session['user'] == 1:
            return render_template('updateUser.html')
        else:
            return render_template('permition.html')
    else:
        return render_template('login.html')

@app.route('/updateUser', methods=['POST'])
def updtUser():
    conn = sqlite3.connect('auditoria.db')
    conn.execute("UPDATE UTILIZADOR set USER = '"+request.form['name']+"' where ID = '"+request.form['id']+"'")
    conn.commit()
    conn.close()
    return redirect(url_for('mainpageAdmin'))

@app.route('/mainpageAdmin/addAuditor')
def addAuditor():
    if 'user' in session:
        if session['user'] == 1:
            return render_template('addAuditor.html')
        else:
            return render_template('permition.html')
    else:
        return render_template('login.html')

@app.route('/addAuditor', methods=['POST'])
def addUser():
    salt = 'esmael'
    p = (request.form['password']+salt).encode()
    #hashed_password = hashlib.sha512(password + salt).hexdigest()
    conn = sqlite3.connect('auditoria.db')
    conn.execute("INSERT INTO AUDITOR (ID, NAME, EMAIL, AGE, ADDRESS) VALUES (?,?,?,?,?) ", \
                (request.form['id'], request.form['name'], request.form['email'], request.form['age'], request.form['address']))
    conn.execute("INSERT INTO UTILIZADOR (ID, USER, PASSWORD, TYPE) VALUES (?,?,?,?) ", \
                (request.form['id'], request.form['user'], hashlib.sha512(p).hexdigest(), request.form['type']))
    conn.commit()
    conn.close()
    return redirect(url_for('mainpageAdmin'))

@app.route('/permition')
def permition():
    return render_template('permition.html')

@app.route('/index')
def logout():
    session.pop('user', None)
    return index()

if __name__ == '__main__':
    app.run(debug = True)
