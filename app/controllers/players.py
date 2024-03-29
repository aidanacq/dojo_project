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



@app.route("/newplayer")
def newplayer():
    if session.get("id") is None:
        return redirect("/")

    if session.get('number') is None:
        session['fname'] = ""
        session['lname'] = ""
        session['number'] = ""
        session['rookie_year'] = ""
        session['last_year'] = ""
    values = {
        "fname": session['fname'],
        "lname": session['lname'],
        "number": session['number'],
        "rookie_year": session['rookie_year'],
        "last_year": session['last_year'],
    }
    return render_template("newplayer.html", values = values, teams = Team.get_all())


@app.route("/newplayerprocess", methods=['POST'])
def newplayerprocess():
    if session.get("id") is None:
        return redirect("/")

    if Player.validate(request.form) == False:
        return redirect("/newplayer")
    session.pop("fname")
    session.pop("lname")
    session.pop("number")
    session.pop("rookie_year")
    session.pop("last_year")

    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "number": request.form['number'],
        "rookie_year": request.form['rookie_year'],
        "last_year": request.form['last_year'],
        "pb": request.form['pb'],
        "team_id": request.form['team'],
    }
    id = Player.new(data)
    rookie = int(request.form['rookie_year'])

    if request.form['pb'] == "pitcher":
        # generate stats for every year between rookie year and last year
        # submit each year to stats table
        for _ in range(rookie, int(request.form['last_year'])+1):
            games = random.randrange(1, 100)
            wins = random.randrange(0, games)
            losses = games-wins
            ip = random.randrange(1, games*9)
            er = random.randrange(0, 7)*games
            era = 9*er/ip
            if str(era).count('.') > 0:
                split = str(era).split('.')
                era = f"{split[0]}.{split[1][0:2]}"
            gs = random.randrange(0, games)
            cg = 0
            if gs > 0:
                cg = random.randrange(0, gs)
            hits = random.randrange(0, 9)*games
            homeruns = 0
            if hits > 0:
                homeruns = random.randrange(0, hits)
            runs = 0
            if er > 0:
                runs = random.randrange(er, er+er)
            so = random.randrange(0, 3)*ip
            bb = random.randrange(0, 5)*ip
            hbp = random.randrange(0, 5)*ip

            stats = {
                "wins": wins,
                "losses": losses,
                "era": era,
                "games": games,
                "ip": ip,
                "gs": gs,
                "cg": cg,
                "hits": hits,
                "homeruns": homeruns,
                "runs": runs,
                "er": er,
                "so": so,
                "bb": bb,
                "hbp": hbp,
                "year": rookie,
                "player_id": id
            }
            Pitcher.new(stats)
            rookie += 1

    elif request.form['pb'] == "batter":
        # generate stats for every year between rookie year and last year
        # submit each year to stats table
        for _ in range(rookie, int(request.form['last_year'])+1):
            games = random.randrange(1, 162)
            pa =  random.randrange(1, 4)*games
            hits = random.randrange(0, pa)
            bb = 0
            if pa-hits > 0:
                bb = random.randrange(0, pa-hits)
            hbp = 0
            if pa-hits-bb > 0:
                hbp = random.randrange(0, pa-hits-bb)
            ab = 0
            if pa-bb-hbp > 0:
                ab = pa-bb-hbp
            runs = 0
            rbi = 0
            homeruns = 0
            if hits > 0:
                homeruns = random.randrange(0, hits)
                runs = random.randrange(homeruns, hits)
                rbi = random.randrange(0, hits)
            so = 0
            if ab-hits > 0:
                so = random.randrange(0, ab-hits)
            obp = ".000"
            if ab+bb+hbp > 0:
                avg = (hits+bb+hbp)/(ab+bb+hbp)
                obp = formatavg(avg)
            ba = ".000"
            if ab > 0:
                avg = hits/ab
                ba = formatavg(avg)

            stats = {
                "games": games,
                "pa": pa,
                "hits": hits,
                "bb": bb,
                "homeruns": homeruns,
                "hbp": hbp,
                "ab": ab,
                "runs": runs,
                "rbi": rbi,
                "so": so,
                "obp": obp,
                "ba": ba,
                "year": rookie,
                "player_id": id
            }
            Batter.new(stats)
            rookie += 1
    else:
        print("error")
    return redirect(f"/teams/{request.form['team']}")


@app.route("/teams/<id>/player_<player_id>/newyear")
def newyear(id, player_id):
    if session.get("id") is None:
        return redirect("/")
    player = Player.get_one(player_id)
    if player.pb == "pitcher":
        # generate an additional year after last year and submit to stats table
        # will also update player's last year to match
        games = random.randrange(1, 100)
        wins = random.randrange(0, games)
        losses = games-wins
        ip = random.randrange(1, games*9)
        er = random.randrange(0, 7)*games
        era = 9*er/ip
        if str(era).count('.') > 0:
            split = str(era).split('.')
            era = f"{split[0]}.{split[1][0:2]}"
        gs = random.randrange(0, games)
        cg = 0
        if gs > 0:
            cg = random.randrange(0, gs)
        hits = random.randrange(0, 9)*games
        homeruns = 0
        if hits > 0:
            homeruns = random.randrange(0, hits)
        runs = 0
        if er > 0:
            runs = random.randrange(er, er+er)
        so = random.randrange(0, 3)*ip
        bb = random.randrange(0, 5)*ip
        hbp = random.randrange(0, 5)*ip

        stats = {
            "wins": wins,
            "losses": losses,
            "era": era,
            "games": games,
            "ip": ip,
            "gs": gs,
            "cg": cg,
            "hits": hits,
            "homeruns": homeruns,
            "runs": runs,
            "er": er,
            "so": so,
            "bb": bb,
            "hbp": hbp,
            "year": int(player.last_year)+1,
            "player_id": player_id
        }
        data ={"id":player_id,"last_year":int(player.last_year)+1}
        Player.update_year(data)
        Pitcher.new(stats)
    else:
        # do the same for batters
        games = random.randrange(1, 162)
        pa =  random.randrange(1, 4)*games
        hits = random.randrange(0, pa)
        bb = 0
        if pa-hits > 0:
            bb = random.randrange(0, pa-hits)
        hbp = 0
        if pa-hits-bb > 0:
            hbp = random.randrange(0, pa-hits-bb)
        ab = 0
        if pa-bb-hbp > 0:
            ab = pa-bb-hbp
        runs = 0
        rbi = 0
        homeruns = 0
        if hits > 0:
            homeruns = random.randrange(0, hits)
            runs = random.randrange(homeruns, hits)
            rbi = random.randrange(0, hits)
        so = 0
        if ab-hits > 0:
            so = random.randrange(0, ab-hits)
        obp = ".000"
        if ab+bb+hbp > 0:
            avg = (hits+bb+hbp)/(ab+bb+hbp)
            obp = formatavg(avg)
        ba = ".000"
        if ab > 0:
            avg = hits/ab
            ba = formatavg(avg)

        stats = {
            "games": games,
            "pa": pa,
            "hits": hits,
            "bb": bb,
            "homeruns": homeruns,
            "hbp": hbp,
            "ab": ab,
            "runs": runs,
            "rbi": rbi,
            "so": so,
            "obp": obp,
            "ba": ba,
            "year": int(player.last_year)+1,
            "player_id": player_id
        }
        data ={"id":player_id,"last_year":int(player.last_year)+1}
        Player.update_year(data)
        Batter.new(stats)
    return redirect(f"/teams/{id}/{player.pb}_{player_id}")


@app.route("/teams/<id>/player_<player_id>/edit")
def edit(id, player_id):
    if session.get("id") is None:
        return redirect("/")
    return render_template("edit.html", player = Player.get_one(player_id), teams = Team.get_all())


@app.route("/teams/<id>/player_<player_id>/editprocess", methods=['POST'])
def editprocess(id, player_id):
    if session.get("id") is None:
        return redirect("/")
    if Player.validate_update(request.form) == False:
        return redirect(f"/teams/{id}/player_{player_id}/edit")
    data = {
        "id": player_id,
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "number": request.form['number'],
        "team_id": request.form['team']
    }
    print(data)
    Player.update(data)
    return redirect(f"/teams/{id}")


@app.route("/teams/<id>/player_<player_id>/delete")
def delete(id, player_id):
    if session.get("id") is None:
        return redirect("/")
    player = Player.get_one(player_id)
    # delete stat tables matching to deleted player first
    if player.pb == "pitcher":
        Pitcher.delete(player_id)
    elif player.pb == "batter":
        Batter.delete(player_id)
    else:
        print("error")
    Player.delete(player_id)
    return redirect(f"/teams/{id}")


def formatavg(avg):
    # turns '0.7642836' into '.764' and turns '0.6' into '.600'
    if len(str(avg)) < 5:
        avg = f"{avg}00000"
    formatted = str(avg)[1:5]
    return formatted