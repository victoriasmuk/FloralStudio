from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask_app import DB
from flask import flash

class Bouquet:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.size = data['size']
        self.uploaded_photo = data['uploaded_photo']

    @classmethod
    def get_with_user(cls, user_id):
        data = {
            'user_id' : user_id,
        }
        query = """
        SELECT * FROM bouquets
        WHERE user_id = %(user_id)s;
        """
        result = connectToMySQL(DB).query_db(query,data)
        return result


    @classmethod
    def save(cls,data):

        query = """
        INSERT INTO bouquets (size, user_id, price, uploaded_photo)
        VALUES (%(size)s, %(user_id)s, %(price)s, %(uploaded_photo)s);
        """
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def find_flowers(cls, suggestions):
        names = []
        for suggestion in suggestions:
            if suggestion["plant_details"]["common_names"] is not None:
                for x in suggestion["plant_details"]["common_names"]:
                    common_name = x
                    names.append(common_name.split())
        plant_name = suggestion["plant_name"]
        names.append(plant_name.split())
        # for suggestion in suggestions:
        #     plant_name = suggestion["plant_name"]
        #     common_name = suggestion["plant_details"]["common_names"][0]
        #     names.append(plant_name.split())
        #     names.append(common_name.split())
        
        list = []
        for a in names:
            list.append(a[0])
        t = tuple(list)
        data = {
            'name': t,
        }
        
        query = """
        SELECT * FROM flowers WHERE name in {}
        """.format(t)
        results = connectToMySQL(DB).query_db(query,data)
        return results
    
    @classmethod
    def get_size(cls,id):
        query = "SELECT size FROM bouquets WHERE id = %(id)s;"
        return connectToMySQL(DB).connection(query,id)

    @staticmethod
    def calculate(data):
        count = 0
        for flower in data['flowers']:
            count += 1
        p = 0
        for flower in data['flowers']:
            p += flower['price']
        if data['bouquet_size'] == "XX-Large":
            qty = 100 / count
        if data['bouquet_size'] == "X-Large":
            qty = 80 / count
        if data['bouquet_size'] == "Large":
            qty = 60 / count
        if data['bouquet_size'] == "Medium":
            qty = 45 / count
        if data['bouquet_size'] == "Small":
            qty = 25 / count
        if data['bouquet_size'] == "X-Small":
            qty = 16 / count
        price = qty * p
        price = '{:,.2f}'.format(price)
        
        
        return price
    
    
    