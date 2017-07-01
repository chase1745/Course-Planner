from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def input():
	return render_template('input.html')

app.run(debug=True)