from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserDetails(db.Model):
  __tablename__ = "UserDetails"
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(32))
  last_name = db.Column(db.String(32))
  username = db.Column(db.String(32))
  city = db.Column(db.String(32))
  password = db.Column(db.String(32))

class UserSearches(db.Model):
  __tablename__ = "UserSearches"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  start_station = db.Column(db.String(32))
  end_station = db.Column(db.String(32))
  
@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    city = request.form.get('city')
    password = request.form.get('password')
    new_user = UserDetails(first_name=first_name, last_name=last_name, username=username, city=city, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main'))
  return render_template('register.html')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')


app.run(host='0.0.0.0', port=81)
