from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'program'

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')


app.run(host='0.0.0.0', port=81)
