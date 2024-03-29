from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_bcrypt import Bcrypt
from app import app
from app.models.user import User
from app.models.team import Team
from app.models.player import Player
from app.models.pitcher import Pitcher
from app.models.batter import Batter
import random
bcrypt = Bcrypt(app)



@app.route("/newteam")
def newteam():
    if session.get("id") is None:
        return redirect("/")

    if session.get('name') is None:
        session["name"] = ""
        session["location"] = ""
    return render_template("newteam.html", name = session['name'], location = session['location'])


@app.route("/newteamprocess", methods=['POST'])
def newteamprocess():
    if session.get("id") is None:
        return redirect("/")

    if Team.validate(request.form) == False:
        return redirect("/newteam")
    session.pop("name")
    session.pop("location")

    data = {
        "name": request.form['name'],
        "location": request.form['location'],
        "champs": 0,
        "winloss": "0/0"
    }
    Team.new(data)
    return redirect("/teams")


@app.route("/teams")
def allteams():
    if session.get("id") is None:
        return redirect("/")
    return render_template("allteams.html", teams = Team.get_all())


@app.route("/teams/<id>")
def oneteam(id):
    if session.get("id") is None:
        return redirect("/")

    pitchers = []
    batters = []

    # assign pitchers and batters to respective lists
    for player in Player.get_all(id):
        if player.get("pb") == "pitcher":
            pitchers.append(player)
        elif player.get("pb") == "batter":
            batters.append(player)
        else:
            print(f"error {player}")
    return render_template("oneteam.html", team = Team.get_one(id), pitchers = pitchers, batters = batters)