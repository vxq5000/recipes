from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.is_valid(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    user_id=User.save(data)
    session['user_id']=user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user=User.get_by_email(request.form)
    if not user:
        flash("Invalid Email! Please sign up!","login")
        return redirect ('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash ("Wrong Password!!","login")
        return redirect ('/')
    session['user_id']=user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), recipes=Recipe.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')