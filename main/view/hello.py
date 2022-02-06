from flask import Blueprint, render_template

bp = Blueprint("hello", __name__, url_prefix="/", static_folder="static")

@bp.route("/")
def ask1():
    return render_template("hello.html")

@bp.route("/analysis")
def ask2():
    return render_template("analysis.html")