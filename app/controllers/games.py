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


@app.route("/game")
def game():
    if session.get("id") is None:
        return redirect("/")
    return render_template("game.html", teams = Team.get_all())


@app.route("/gameprocess", methods=['POST'])
def gameprocess():
    if session.get("id") is None:
        return redirect("/")
    if request.form['team1'] == request.form['team2']:
        flash("Teams cannot be the same.")
        return redirect("/game")
    pitchers1 = []
    batters1 = []
    pitchers2 = []
    batters2 = []
    team1 = Team.get_one(request.form['team1'])
    team2 = Team.get_one(request.form['team2'])

    # separates batters and pitchers from each team into lists
    for player in Player.get_all(team1.id):
        if player.get("pb") == "pitcher":
            pitchers1.append(player)
        elif player.get("pb") == "batter":
            batters1.append(player)
        else:
            print(f"error {player}")

    for player in Player.get_all(team2.id):
        if player.get("pb") == "pitcher":
            pitchers2.append(player)
        elif player.get("pb") == "batter":
            batters2.append(player)
        else:
            print(f"error {player}")

    total_pitch_runs1 = 0
    total_pitch_runs2 = 0
    total_bat_runs1 = 0
    total_bat_runs2 = 0

    # counts total runs scored and allowed by each team
    # this counts every player's stats from every year
    for pitcher in pitchers1:
        stats = Pitcher.get_all(pitcher.get('id'))
        for statline in stats:
            total_pitch_runs1 = total_pitch_runs1 + int(statline.get('runs'))
    for pitcher in pitchers2:
        stats = Pitcher.get_all(pitcher.get('id'))
        for statline in stats:
            total_pitch_runs2 = total_pitch_runs2 + int(statline.get('runs'))
    for batter in batters1:
        stats = Batter.get_all(batter.get('id'))
        for statline in stats:
            total_bat_runs1 = total_bat_runs1 + int(statline.get('runs'))
    for batter in batters2:
        stats = Batter.get_all(batter.get('id'))
        for statline in stats:
            total_bat_runs2 = total_bat_runs2 + int(statline.get('runs'))

    # number used for deciding who wins
    r = random.randrange(1,6)
    # chance is determined by the difference between runs scored and allowed by a team
    team1chance = total_bat_runs1 - total_pitch_runs1
    team2chance = total_bat_runs2 - total_pitch_runs2
    # team with a higher number has a 3/5 chance of winning, lower number is a 2/5 chance
    if team1chance > team2chance:
        if r > 2:
            winner = team1.id
            loser = team2.id
        else:
            winner = team2.id
            loser = team1.id
    elif team2chance > team1chance:
        if r > 2:
            winner = team2.id
            loser = team1.id
        else:
            winner = team1.id
            loser = team2.id

    # randomly decide score, making sure winner score is always greater
    winner_score = random.randrange(1, 15)
    loser_score = random.randrange(0, winner_score)

    # add a win to winning team's record
    split = str(Team.get_one(winner).winloss).split("/")
    data = {"id":winner, "winloss":f"{int(split[0])+1}/{split[1]}"}
    Team.update_winloss(data)

    # add a loss to losing team's record
    split = str(Team.get_one(loser).winloss).split("/")
    data = {"id":loser, "winloss":f"{split[0]}/{int(split[1])+1}"}
    Team.update_winloss(data)

    # if the game was checked as a world series game, add a champ win to winning team
    if request.form.get('ws'):
        data = {"id":winner, "champs":int(Team.get_one(winner).champs)+1}
        Team.update_champs(data)
    return redirect(f"/gameresults/{winner}/{loser}/{winner_score}/{loser_score}")


@app.route("/gameresults/<winner>/<loser>/<winner_score>/<loser_score>")
def gameresults(winner, loser, winner_score, loser_score):
    if session.get("id") is None:
        return redirect("/")
    return render_template("gameresults.html", winner_score = winner_score, loser_score = loser_score, winning_team = Team.get_one(winner), losing_team = Team.get_one(loser))