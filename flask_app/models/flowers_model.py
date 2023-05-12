from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask_app.models import bouquets_model
from flask_app import DB
from flask import flash

class Flower:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.category = data['category']

    @classmethod
    def get_all(cls):
        query = 'SELECT flowers.*, format(price, 2) AS money FROM flowers ORDER BY name;'
        results = connectToMySQL(DB).query_db(query)
        return results
