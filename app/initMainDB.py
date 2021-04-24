import csv

#from app import app

from models import db, Ingredient, Recipe
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.mainDB.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()
db.create_all(app=app)

with open("data/recipes.csv") as recipe_file:
    recipe_data = csv.DictReader(recipe_file)

    for rd in recipe_data:
        new_recipe = Recipe(name=rd['Compound Ingredient Name'], category=rd['Category'], ingredientsList=rd['Contituent Ingredients'])
        db.session.add(new_recipe)

with open("data/ingredients.csv") as ingre_file:
    ingre_data = csv.DictReader(ingre_file)

    for iData in ingre_data:
        new_ingre = Ingredient(name=iData['Aliased Ingredient Name'], category=iData['Category'])
        db.session.add(new_ingre)

db.session.commit()
print("Database ready")

