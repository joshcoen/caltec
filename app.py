from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import MySQLdb

app = Flask(__name__)

if __name__ == '__main__':
    db = MySQLdb.connect(host="mysql", user="root", passwd="JAC2ufc1", db="login")
    cur = db.cursor()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class ServerError(Exception):pass

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('login'))

    username_session = escape(session['username']).capitalize()
    return render_template('index.html', session_user_name=username_session)

@app.route('/login', methods=['GET', 'POST'])

def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        print username_form
        cur.execute("SELECT COUNT(1) FROM users WHERE user_name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT user_pass FROM users WHERE user_name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                print row[0]
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Username"
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
