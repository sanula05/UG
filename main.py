from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import networkx as nx
import matplotlib.pyplot as plt
import tube as t

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

@app.route('/main',methods=['GET', 'POST'])
# @login_required
def main():
   if request.method == 'POST':
     start_point = request.form["start_point"]
     end_point = request.form["end_point"]
     session["start_point"] = start_point
     session["end_point"] = end_point
     return redirect(url_for("result"))
   else:
     return render_template('main.html')

@app.route('/result')
def result():
  if "start_point" and "end_point" in session:
    start_point = session["start_point"]
    end_point = session["end_point"]
    return(nx.dijkstra_path(tube_map,start_point,end_point))
    
    
  else:
   return redirect(url_for("main"))
    
  
    # return render_template('result.html')

@app.route('/login')
def login():
    return render_template('login.html')


app.run(host='0.0.0.0', port=81)
