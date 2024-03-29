from app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Player:
    DB = "baseballstats"
    def __init__( self , data ):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.number = data['number']
        self.rookie_year = data['rookie_year']
        self.last_year = data['last_year']
        self.pb = data['pb']
        self.team_id = data["team_id"]

    @classmethod
    def get_all(cls, id):
        query = f"SELECT * FROM players WHERE team_id = {id};"
        results = connectToMySQL(cls.DB).query_db(query)
        players = []
        for player in results:
            players.append(player)
        return players

    @classmethod
    def new(cls, data):
        query = """INSERT INTO players (fname,lname,number,rookie_year,last_year,pb,team_id)
                VALUES (%(fname)s,%(lname)s,%(number)s,%(rookie_year)s,%(last_year)s,%(pb)s,%(team_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM players WHERE id = %(id)s;"
        data = {'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = """UPDATE players
                SET fname=%(fname)s,lname=%(lname)s,number=%(number)s,team_id=%(team_id)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update_year(cls,data):
        query = """UPDATE players
                SET last_year=%(last_year)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM players WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate(form):
        is_valid = True
        if form['fname'] == "" or form['lname'] == "" or form['number'] == "" or form['rookie_year'] == "" or form['last_year'] == "":
            flash("All fields must be filled out.")
            is_valid = False
            session["fname"] = form['fname']
            session["lname"] = form['lname']
            session["number"] = form['number']
            session['rookie_year'] = form['rookie_year']
            session['last_year'] = form['last_year']
            return is_valid

        if len(form['fname']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False

        if len(form['lname']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        if form['number'].isdigit() == False:
            flash("Jersey number must be a valid number.")
            is_valid = False

        if len(form['number']) > 2 or len(form['number']) < 1:
            flash("Jersey number must be between 0-99.")
            is_valid = False

        if len(form['rookie_year']) > 4 or len(form['last_year']) > 4 or len(form['rookie_year']) < 4 or len(form['last_year']) < 4:
            flash("Years must be 4 digits big.")
            is_valid = False

        if form['rookie_year'].isdigit() == False or form['last_year'].isdigit() == False:
            flash("Years must be a valid number.")
            is_valid = False
        else:
            if int(form['rookie_year']) >= int(form['last_year']):
                flash("Rookie year must come before last year.")
                is_valid = False

        if is_valid == False:
            session["fname"] = form['fname']
            session["lname"] = form['lname']
            session["number"] = form['number']
            session["rookie_year"] = form['rookie_year']
            session["last_year"] = form['last_year']
        return is_valid

    @staticmethod
    def validate_update(form):
        is_valid = True
        if form['fname'] == "" or form['lname'] == "" or form['number'] == "":
            flash("All fields must be filled out.")
            is_valid = False
            session["fname"] = form['fname']
            session["lname"] = form['lname']
            session["number"] = form['number']
            return is_valid

        if len(form['fname']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False

        if len(form['lname']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        if form['number'].isdigit() == False:
            flash("Jersey number must be a valid number.")
            is_valid = False

        if len(form['number']) > 2 or len(form['number']) < 1:
            flash("Jersey number must be between 0-99.")
            is_valid = False

        if is_valid == False:
            session["fname"] = form['fname']
            session["lname"] = form['lname']
            session["number"] = form['number']
        return is_valid