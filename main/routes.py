from flask import Blueprint, render_template, session, request, redirect
from models import snippet_model

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def landing():
    # If user is logged in, redirect to home page
    if "user_id" in session:
        return redirect("/home")

    return render_template("landing.html")


@main_bp.route("/home")
def home():
    # If user is not logged in, redirect to login page
    if "user_id" not in session:
        return redirect("/login")

    q = request.args.get("q", "").strip()

    if q:
        snippets = snippet_model.search_snippets(q)
    else:
        snippets = snippet_model.get_all_snippets_with_users()

    return render_template("home.html", snippets=snippets, q=q)
