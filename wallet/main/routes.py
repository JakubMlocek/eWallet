from flask import render_template, request, Blueprint
from wallet.database_connector import Transaction

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")