from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import networkx as nx
import matplotlib.pyplot as plt
import tube as t
from werkzeug.security import generate_password_hash, check_password_hash



tube_map = nx.Graph()
for station in t.tube_data.keys():
    tube_map.add_node(station)

for start_station, connections in t.tube_data.items():
    for end_station, distance in connections.items():
        tube_map.add_edge(start_station, end_station, weight=distance)

app = Flask(__name__)
app.secret_key = "hello_wrld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'Mattisthebestprogrammerintheworld!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class UserDetails(UserMixin,db.Model):
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

@login_manager.user_loader
def load_user(user_id):
  return UserDetails.query.get(int(user_id))
  
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
    hashed_password = generate_password_hash(password)
    new_user = UserDetails(first_name=first_name, last_name=last_name, username=username, city=city, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    login()
    return redirect(url_for('main'))
  return render_template('register.html')

@app.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('main'))
  else:
    return redirect(url_for('login'))

@app.route('/main',methods=['GET', 'POST'])
@login_required
def main():

   stations=[]
   for station in t.tube_data.keys():
     stations.append(station)
     
   if request.method == 'POST':
     start_point = request.form["start_point"]
     end_point = request.form["end_point"]
     session["start_point"] = start_point
     session["end_point"] = end_point
     return redirect(url_for("result"))
   else:
     return render_template('main.html', stations=stations, current_user=current_user)
@login_required
@app.route('/result',methods=['GET', 'POST'])
def result():
  if "start_point" and "end_point" in session:
    start_point = session["start_point"]
    end_point = session["end_point"]
    stations = nx.dijkstra_path(tube_map,start_point,end_point)
    cost = (nx.dijkstra_path_length(tube_map,start_point,end_point))*5
    rounded_cost = round(cost, 2)
    return render_template('result.html', stations=stations, cost=rounded_cost)
    
    
  else:
   return redirect(url_for("main"))
    
  
    # return render_template('result.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main'))
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    user = UserDetails.query.filter_by(username=username).first()
    print(user)
    if user:
      if check_password_hash(user.password, password):
        login_user(user)
        session['username'] = current_user.username
        session['first_name'] = current_user.first_name
        session['last_name'] = current_user.last_name
        return redirect(url_for('main'))
      else:
        return render_template('login.html', error='Wrong username or password')
        
  
  
  return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
app.run(host='0.0.0.0', port=81)
