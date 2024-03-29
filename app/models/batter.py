from app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Batter:
    DB = "baseballstats"
    def __init__( self , data ):
        self.id = data['id']
        self.games = data['games']
        self.pa = data['pa']
        self.hits = data['hits']
        self.bb = data['bb']
        self.homeruns = data['homeruns']
        self.hbp = data['hbp']
        self.ab = data["ab"]
        self.runs = data['runs']
        self.rbi = data['rbi']
        self.so = data['so']
        self.obp = data['obp']
        self.ba = data['ba']
        self.player_id = data['player_id']

    @classmethod
    def get_all(cls, id):
        query = f"SELECT * FROM batterstats WHERE player_id = {id};"
        results = connectToMySQL(cls.DB).query_db(query)
        allstats = []
        for statline in results:
            allstats.append(statline)
        return allstats

    @classmethod
    def new(cls, data):
        query = """INSERT INTO batterstats (games,pa,hits,bb,homeruns,hbp,ab,runs,rbi,so,obp,ba,year,player_id)
                VALUES (%(games)s,%(pa)s,%(hits)s,%(bb)s,%(homeruns)s,%(hbp)s,%(ab)s,%(runs)s,%(rbi)s,%(so)s,%(obp)s,%(ba)s,%(year)s,%(player_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM batterstats WHERE id = %(id)s;"
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
        query  = "DELETE FROM batterstats WHERE player_id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)