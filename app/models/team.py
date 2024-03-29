from app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Team:
    DB = "baseballstats"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.champs = data['champs']
        self.winloss = data['winloss']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM teams;"
        results = connectToMySQL(cls.DB).query_db(query)
        teams = []
        for team in results:
            teams.append(team)
        return teams

    @classmethod
    def new(cls, data):
        query = """INSERT INTO teams (name,location,champs,winloss)
                VALUES (%(name)s,%(location)s,%(champs)s,%(winloss)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM teams WHERE id = %(id)s;"
        data = {'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_champs(cls,data):
        query = """UPDATE teams
                SET champs=%(champs)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update_winloss(cls,data):
        query = """UPDATE teams
                SET winloss=%(winloss)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM teams WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate(form):
        is_valid = True
        if form['name'] == "" or form['location'] == "":
            flash("All fields must be filled out.")
            is_valid = False
            session["name"] = form['name']
            session["location"] = form['location']
            return is_valid

        if len(form['name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False

        if len(form['location']) < 2:
            flash("Location must be at least 2 characters.")
            is_valid = False

        if is_valid == False:
            session["name"] = form['name']
            session["location"] = form['location']
        return is_valid