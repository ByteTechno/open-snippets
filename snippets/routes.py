from flask import Blueprint, render_template, request, redirect, session, abort
from models import snippet_model
import sqlite3

snippets_bp = Blueprint('snippets', __name__)

@snippets_bp.route("/add", methods=["GET", "POST"])
def add_snippet():
    # If not logged in, redirect to login
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        user_id = session["user_id"]

        snippet_model.add_snippet(user_id, title, content)

        return redirect("/")
    return render_template("add.html")


@snippets_bp.route("/my-snippets")
def my_snippets():
    # If not logged in, redirect to login
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    my_snips = snippet_model.get_snippets_by_user(user_id)
    return render_template("my_snippets.html", snippets=my_snips)


@snippets_bp.route("/delete/<int:snippet_id>", methods=["POST"])
def delete_snippet(snippet_id):
    # If not logged in, redirect to login
    if "user_id" not in session:
        return redirect("/login")

    snippet_model.delete_snippet(snippet_id, session["user_id"]) 
    return redirect("/my-snippets")

@snippets_bp.route("/edit/<int:snippet_id>", methods=["GET", "POST"])
def edit_snippet(snippet_id):
    # If not logged in, redirect to login
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        snippet_model.update_snippet(snippet_id, session["user_id"], title, content)

        return redirect("/my-snippets")

    snippet = snippet_model.get_snippet_by_id(snippet_id)

    # Security Check: Ownership verification
    if not snippet:
        abort(404)
    if snippet['user_id'] != session["user_id"]:
        abort(403)

    return render_template("edit.html", snippet=snippet)
    
@snippets_bp.route("/snippet/<int:snippet_id>")
def snippet_detail(snippet_id):
    # If not logged in, redirect to login
    if "user_id" not in session:
        return redirect("/login")

    snippet = snippet_model.get_snippet_by_id(snippet_id)

    if not snippet:
        abort(404)

    return render_template("snippet_detail.html", snippet=snippet)
