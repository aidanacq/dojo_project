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


@app.route("/teams/<id>/batter_<player_id>")
def batter(id, player_id):
    if session.get("id") is None:
        return redirect("/")
    return render_template("batter.html", batters = Batter.get_all(player_id), player = Player.get_one(player_id), id = id)