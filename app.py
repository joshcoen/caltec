from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import MySQLdb

app = Flask(__name__)

if __name__ == '__main__':
    db = MySQLdb.connect(host="mysql", user="root", passwd="JAC2ufc1", db="login")
    cur = db.cursor()

class ServerError(Exception):pass

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username'])
        return render_template('index.html', session_user_name=username_session)

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])

def login():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            username_form  = request.form['username']
            cur.execute("SELECT COUNT(1) FROM users WHERE user_name = %s;", [username_form])

            if not cur.fetchone()[0]:
                raise ServerError('Invalid username')

            password_form  = request.form['password']
            cur.execute("SELECT user_pass FROM users WHERE user_name = %s;", [username_form])

            for row in cur.fetchall():
                if md5(password_form).hexdigest() == md5(row[0]).hexdigest():
                    session['username'] = username_form
                    return redirect(url_for('index'))

            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/cal')
def cal():
    return render_template('cal.html')

app.secret_key = 'T0Gr98j/3yX R~XHH!jmN]LWX/,?89'

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
