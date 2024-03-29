from app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Pitcher:
    DB = "baseballstats"
    def __init__( self , data ):
        self.id = data['id']
        self.games = data['games']
        self.wins = data['wins']
        self.losses = data['losses']
        self.ip = data['ip']
        self.er = data['er']
        self.era = data['era']
        self.gs = data["gs"]
        self.cg = data['cg']
        self.hits = data['hits']
        self.homeruns = data['homeruns']
        self.runs = data['runs']
        self.so = data['so']
        self.bb = data['bb']
        self.hbp = data['hbp']

    @classmethod
    def get_all(cls, id):
        query = f"SELECT * FROM pitcherstats WHERE player_id = {id};"
        results = connectToMySQL(cls.DB).query_db(query)
        allstats = []
        for statline in results:
            allstats.append(statline)
        return allstats

    @classmethod
    def new(cls, data):
        query = """INSERT INTO pitcherstats (games,wins,losses,ip,er,era,gs,cg,hits,homeruns,runs,so,bb,hbp,year,player_id)
                VALUES (%(games)s,%(wins)s,%(losses)s,%(ip)s,%(er)s,%(era)s,%(gs)s,%(cg)s,%(hits)s,%(homeruns)s,%(runs)s,%(so)s,%(bb)s,%(hbp)s,%(year)s,%(player_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM pitcherstats WHERE id = %(id)s;"
        data = {'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = """UPDATE recipes
                SET name=%(name)s,description=%(description)s,instructions=%(instructions)s,date=%(date)s,under=%(under)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM pitcherstats WHERE player_id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)