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



@app.route("/test")
def test():
    return redirect("/")


@app.route("/")
def default():
    if session.get('fname') is None:
        session['fname'] = ""
        session['lname'] = ""
        session['email'] = ""
    return render_template("default.html", fname = session['fname'], lname = session['lname'], email = session['email'])


@app.route("/regprocess", methods=['POST'])
def regprocess():
    if User.validate_reg(request.form) == False:
        return redirect("/")
    else:
        session.pop('fname', None)
        session.pop('lname', None)
        session.pop('email', None)

        hashpass = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "fname": request.form["fname"],
            "lname": request.form["lname"],
            "email": request.form["email"],
            "password": hashpass
        }
        session['id'] = User.new(data)
    return redirect("/teams")


@app.route("/logprocess", methods=['POST'])
def logprocess():
    user_in_db = User.get_email(request.form['email'])
    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect("/")
    session.pop("fname")
    session.pop("lname")
    session.pop("email")
    session['id'] = user_in_db.id
    return redirect("/teams")


@app.route("/logout")
def logout():
    if session.get("id") is None:
        return redirect("/")
    session.clear()
    return redirect("/")