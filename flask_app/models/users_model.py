from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import bcrypt, DB

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def find_one_by_email(cls, email):
        data = {
            'email' : email,
        }
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return False
    
    @classmethod
    def get_user_by_id(cls, id):
        data = {
            'id' : id,
        }
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def create(cls,form):
        data = {
            **form,
            'password' : bcrypt.generate_password_hash(form['password'])
        }
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        result = connectToMySQL(DB).query_db(query,data)
        new_user = cls.get_user_by_id(result)
        return new_user
    
    @classmethod
    def update(cls,data):
        query = """
        UPDATE users SET
        first_name = %(first_name)s,
        last_name = %(last_name)s,
        email = %(email)s
        WHERE id = %(id)s;
        """
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users ORDER BY first_name;'
        results = connectToMySQL(DB).query_db(query)
        list = []
        for user in results:
            list.append( cls(user) )
        return list
    
    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        result = connectToMySQL(DB).query_db(query,id)
        return result
    
    @classmethod
    def get_most_recent(cls):
        query = """
        SELECT * FROM users ORDER BY users.id DESC LIMIT 1;
        """
        results = connectToMySQL(DB).query_db(query)
        result = results[0]
        return cls(result)

    @classmethod
    def login(cls,form):
        found_user = cls.find_one_by_email(form['email'])
        if found_user:
            if bcrypt.check_password_hash(found_user.password, form['password']):
                return found_user
            else:
                flash('Invalid Login! Wrong password!')
                return False
        else:
            flash('Invalid Login')
            return False

    @staticmethod
    def validate_update(form):
        is_valid = True
        if len(form['first_name']) <= 2:
            is_valid = False
            flash('Invalid First Name! Must be at least 2 characters.')
        if not form['first_name'].isalpha():
            is_valid = False
            flash('Invalid First Name! Must contain only letters.')
        if len(form['last_name']) <= 2:
            is_valid = False
            flash('Invalid last Name! Must be at least 2 characters.')
        if not form['last_name'].isalpha():
            is_valid = False
            flash('Invalid Last Name! Must contain only letters.')
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            flash('This email address is invalid.')
        return is_valid


    @staticmethod
    def validate(form):
        is_valid = True
        if len(form['first_name']) <= 2:
            is_valid = False
            flash('Invalid First Name! Must be at least 2 characters.')
        if not form['first_name'].isalpha():
            is_valid = False
            flash('Invalid First Name! Must contain only letters.')
        if len(form['last_name']) <= 2:
            is_valid = False
            flash('Invalid last Name! Must be at least 2 characters.')
        if not form['last_name'].isalpha():
            is_valid = False
            flash('Invalid Last Name! Must contain only letters.')
        if User.find_one_by_email(form['email']):
            is_valid = False
            flash("User with this email already exists!")
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            flash('This email address is invalid.')
        if not PW_REGEX.match(form['password']):
            is_valid = False
            flash('Inavlid Password! Must include: a minimum of 8 characters, at least one uppercase letter, one lowercase letter, one number and one special character.')
        if form['password'] != form['confirm_password']:
            is_valid = False
            flash("Passwords don't match!")
        return is_valid

