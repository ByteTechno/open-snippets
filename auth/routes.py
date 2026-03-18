from flask import Blueprint, render_template, request, redirect, session
import bcrypt
from models import user_model

auth_bp = Blueprint('auth', __name__)

# Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = user_model.get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode("utf-8"), user[1]):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect("/")
        else:
            error = "Invalid username or password. Please try again."

    return render_template("login.html", error=error)


# Register
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            user_model.create_user(username, hashed_password)
            return redirect("/login")
        except:
            error = "Username already exists. Please choose another one."

    return render_template("register.html", error=error)


# Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
