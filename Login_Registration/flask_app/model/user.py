from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



class User:
    db = "login_registration"
    def __init__(self,users):
        self.id = users['id']
        self.name = users['name']
        self.email = users['email']
        self.password = users['password']
        self.created_At = users['created_At']
        self.updated_At = users['updated_At']

    @classmethod
    def save(cls, users):
        query = "INSERT INTO login_registration.users (name,email,password) VALUES(%(name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query, users)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM login_registration.users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append (cls(row))
        return users

    @classmethod
    def get_email(cls, users):
        query = "SELECT * FROM login_registration.users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,users)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_id(cls, users):
        query = "SELECT * FROM login_registration.users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,users)
        return cls(results[0])

    @staticmethod
    def validate(users):
        is_valid = True
        query = "SELECT * FROM login_registration.users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,users)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(users['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(users['name']) < 4:
            flash("name must be at least 4 characters","register")
        if len(users['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if users['password'] != users['confirm']:
            flash("Passwords don't match","register")
        return is_valid