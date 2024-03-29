from app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class User:
    DB = "baseballstats"
    def __init__( self , data ):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(user)
        return users

    @classmethod
    def new(cls, data):
        query = """INSERT INTO users (fname,lname,email,password)
    		    VALUES (%(fname)s,%(lname)s,%(email)s,%(password)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, user_id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id':user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return (results[0])

    @classmethod
    def update(cls,data):
        query = """UPDATE users
                SET first_name=%(fname)s,last_name=%(lname)s,email=%(email)s,updated_at=%(updated)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_email(cls, email):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email':email}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_reg(form):
        is_valid = True
        if form['fname'] == "" or form['lname'] == "" or form['email'] == "" or form['password'] == "" or form['confpassword'] == "":
            flash("All fields must be filled out.")
            is_valid = False
            session["fname"] = form['fname']
            session["lname"] = form['lname']
            session["email"] = form['email']
            return is_valid

        if len(form['fname']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False

        if len(form['lname']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False

        if any(char.isdigit() for char in form['fname']) or any(char.isdigit() for char in form['lname']):
            flash("Name cannot contain numbers.")
            is_valid = False

        if User.get_email(form['email']) != False:
            flash("Email already in use.")
            is_valid = False

        if form['email'][len(form['email']) - 4:] != ".com":
            flash("Email must end in '.com'.")
            is_valid = False

        if len(form['password']) < 8:
            flash("Password must be at least eight characters long.")
            is_valid = False

        if form['password'] != form['confpassword']:
            flash("Passwords do not match.")
            is_valid = False

        if not any(char.isdigit() for char in form['password']) or not any(char.isupper() for char in form['password']):
            flash("Password must contain at least one number and one capital letter.")
            is_valid = False

        if is_valid == False:
            session["fname"] = form['fname']
            session["lname"] = form['lname']
            session["email"] = form['email']
        return is_valid