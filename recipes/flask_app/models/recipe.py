from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.quick=data['quick']
        self.date_made=data['date_made']
        self.description=data['description']
        self.instructions=data['instructions']
        self.created_on=data['created_on']
        self.updated_on=data['updated_on']
        self.user_id=data['user_id']

    @classmethod
    def save(cls,data):
        query="INSERT INTO recipes (name, quick, date_made, description, instructions, user_id) VALUES (%(name)s,%(quick)s,%(date_made)s,%(description)s,%(instructions)s,%(user_id)s);"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def get_all(cls):
        query="SELECT * FROM recipes;"
        results= connectToMySQL('recipes').query_db(query)
        recipes=[]
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM recipes WHERE id=%(id)s"
        results=connectToMySQL('recipes').query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query="UPDATE recipes SET name=%(name)s, quick=%(quick)s,description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s,updated_on=NOW() WHERE id=%(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @staticmethod
    def is_valid(recipe):
        is_valid=True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Decription must be at least 3 characters")
        if len(recipe['instructions']) < 3:
            is_valid=False
            flash ("Instructions must be at least 3 characters")
        return is_valid   