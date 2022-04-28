from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    user_data={
        "id":session['user_id']
    }
    return render_template("show.html", recipe=Recipe.get_one(data), user=User.get_by_id(user_data))

@app.route('/create/recipe', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.is_valid(request.form):
        return redirect ('/recipes/new')
    data={
        "name":request.form["name"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "quick":int(request.form["quick"]),
        "date_made":request.form["date_made"],
        "user_id":session["user_id"]
    }
    Recipe.save(data)
    return redirect ('/dashboard')

@app.route('/recipes/new')
def create():
    if 'user_id' not in session:
        return redirect ('/')
    data={
        "id":session['user_id']
    }
    return render_template('add.html', user=User.get_by_id(data))

@app.route('/recipes/edit/<int:id>')
def editrecipes(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    user_data={
        "id":session['user_id']
    }
    return render_template("edit.html",user=User.get_by_id(user_data), recipe=Recipe.get_one(data))

@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.is_valid(request.form):
        return redirect ('/recipes/new')
    data={
        "name":request.form["name"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "quick":request.form["quick"],
        "date_made":request.form["date_made"],
        "id":request.form["id"]
    }
    Recipe.update(data)
    return redirect ('/dashboard')

@app.route('/recipes/destroy/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect('/dashboard')