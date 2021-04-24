import json
from flask_login import UserMixin, LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db=SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    myRecipes = db.relationship('MyRecipe', backref="myrecipe", lazy=True)
    myIngredients = db.relationship('MyIngredient', backref='myingredient', lazy=True)

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }
    
    #hashes the password parameter and stores it in the object
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    #Returns true if the parameter is equal to the object’s password property
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #To String method
    def __repr__(self):
        return '<User {}>'.format(self.username)  



class Ingredient(db.Model):
    ingredientID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))

    def toDict(self):
        return {
            "ingredientID": self.ingredientID,
            "name": self.name,
            "category": self.category
        }
        
class Recipe(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    #ingredients = db.relationship('Ingredient', backref='ingredient', lazy=True)
    ingredientsList = db.Column(db.String(100))

    def toDict(self):
        return {
            "rid": self.rid,
            "name": self.name,
            "category": self.category
        }

class MyRecipe(db.Model):
    myRecipeID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipeID = db.Column(db.Integer, db.ForeignKey('recipe.rid'), nullable=False)
    recipes = db.relationship('Recipe', backref='recipe', lazy=True)
    name = db.Column(db.String(50))

    def toDict(self):
        return {
            "myRecipeID": self.myRecipeID,
            "userID": self.userID,
            "recipeID": self.recipeID,
            "name": self.name
        }
    
class MyIngredient(db.Model):
    myIngredientID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredientID = db.Column(db.Integer, db.ForeignKey('ingredient.ingredientID'), nullable=False)
    ingredients = db.relationship('Ingredient', backref='ingredient', lazy=True)
    name = db.Column(db.String(50))

    def toDict(self):
        return{
            "myIngredientID": self.ingredientID,
            "userID": self.userID,
            "name": self.name
        }