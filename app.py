from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def home():
	return "Hey there"

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
