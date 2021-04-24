from app import app
import json
#from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from sqlalchemy.exc import IntegrityError
import os
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from .models import db, Recipe, Ingredient, MyRecipe, MyIngredient, User
from .forms import SignUp, LogIn
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import UserMixin

from . import login_manager

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route("/settings")
@login_required
def settings():
  pass

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('index')) 

@app.route('/')
def index():
    if current_user.is_authenticated:
      recipes = Recipe.query.order_by(Recipe.name)
    else:  
      recipes = Recipe.query.limit(50)
    return render_template("/public/index.html", recipes=recipes )

@app.route('/login', methods=['GET'])
def loginPage():
  form = LogIn()
  return render_template('/public/login.html', form=form)

@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return redirect(url_for('index')) # redirect to main page if login successful
  flash('Invalid credentials')
  return redirect(url_for('loginPage'))

@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('/public/signup.html', form=form) # pass form object to template

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username'], email=data['email']) # create user object
    newuser.set_password(data['password']) # set password
    db.session.add(newuser) # save new user
    db.session.commit()
    flash('Account Created!')# send message
    return redirect(url_for('index'))# redirect to login page
  flash('Error invalid input!')
  return redirect(url_for('signup')) 

@app.route('/bob')
@login_required
def printName():
    print(current_user.get_id())
    return redirect(request.referrer)

@app.route('/test')
def test():
    data = Recipe.query.all()
    data = [recipe.toDict() for recipe in data]
    
    return json.dumps(data)

@app.route('/addtofav/<n>')
@login_required
def test2(n):
    rec = Recipe.query.get(n)
    newMyRec = MyRecipe(userID=current_user.get_id(), recipeID=n, name=rec.name)
    query = MyRecipe.query.filter_by(userID=current_user.get_id(), recipeID=n)
    if query.count() < 1:
      db.session.add(newMyRec)
      db.session.commit()
      flash('Recipe Added')
      return redirect(url_for('index'))
    else:
      flash('Recipe Already Added!')
      return redirect(url_for('index'))


@app.route('/myrecipe')
def view_rec():
    rec = MyRecipe.query.filter_by(userID=1).all()
    data = [recipe.toDict() for recipe in rec]

    return json.dumps(data)

@app.route('/addsepingr/<n>')
@login_required
def addingr(n):
    rec = Ingredient.query.get(n)
    newMyRec = MyIngredient(userID=current_user.get_id(), ingredientID=n, name=rec.name)
    query = MyIngredient.query.filter_by(userID=current_user.get_id(), ingredientID=n)
    if query.count() < 1:
      db.session.add(newMyRec)
      db.session.commit()
      flash('Ingredient Added')
      return redirect(url_for('displaygList'))
    else:
      flash('Ingredient Already Added')
      return redirect(url_for('displaygList'))

@app.route('/gList')
@login_required
def displaygList():
    MI_data = MyIngredient.query.filter_by(userID = current_user.get_id()).all()
    I_data = Ingredient.query.order_by(Ingredient.name)
    MR_data = MyRecipe.query.filter_by(userID = current_user.get_id()).all()
    return render_template("/public/gList.html", myingredients = MI_data , ingredients = I_data , myrecipes = MR_data )

@app.route('/myingredient/<n>')
@login_required
def deleteingr(n):
    result = MyIngredient.query.get(n)
    try:
      db.session.delete(result)
      db.session.commit()
      return redirect(url_for('displaygList'))
    except:
          return redirect(url_for('displaygList'))

@app.route('/removefav/<n>')
@login_required
def deleteFav(n):
  result = MyRecipe.query.get(n)
  try:
      db.session.delete(result)
      db.session.commit()
      return redirect(url_for('displaygList'))
  except:
          return redirect(url_for('displaygList'))

@app.route('/addrecipebased/<n>')
@login_required
def bigBoy(n):
  result = Recipe.query.get(n)
  ingredients = result.ingredientsList.split(',')
  for x in ingredients:
    if '=' in x:
      x = x.replace("=", " ")
    data = Ingredient.query.filter_by(name = x ).first()
    if data is not None:
      new_data = MyIngredient.query.filter_by(userID=current_user.get_id(), name = x )
      if new_data.count() < 1:
        newMyRec = MyIngredient(userID=current_user.get_id(), ingredientID=data.ingredientID, name=data.name)  
        db.session.add(newMyRec)
    else:
      new_ingre = Ingredient(name=x, category='custom')
      db.session.add(new_ingre)
      db.session.commit()
      newMyRec = MyIngredient(userID=current_user.get_id(), ingredientID=new_ingre.ingredientID, name=new_ingre.name)
      db.session.add(newMyRec)
  db.session.commit()
  return redirect(url_for('displaygList'))
       
      

  