"""
There will be flask api for this app
"""
import os
import configparser

from flask import Flask, jsonify, request, url_for, redirect, render_template

from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.wallet.wallet_factory import WalletFactory

_config = configparser.ConfigParser()
_config.read(os.path.join(os.getcwd(), "configuration", "equipment.ini"))

app = Flask(__name__)

# TODO Swagger
# from flask_swagger_ui import get_swaggerui_blueprint
#
# SWAGGER_URL="/swagger"
# API_URL="/static/swagger.json"
#
# swagger_ui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': 'Access API'
#     }
# )
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("Login") == "Login":
            username = request.form.get("username")
            password = request.form.get("password")
            if not db_session.query(User).filter(User.user_id == username).first():
                print(f"There is no user with username: {username}")
                return render_template("index.html")
            db_user: User = db_session.query(User).filter(User.user_id == username).first()
            if not db_user.verify_password(password):
                print("Wrong password!")
                return render_template("index.html")
            return redirect(url_for("user", username=username))

        if request.form.get("Register") == "Register":
            username = request.form.get("username")
            password = request.form.get("password")
            if db_session.query(User).filter(User.user_id == username).first():
                print("USER EXIST!")
                return render_template("index.html")
            db_session.add(User(username, password, float(_config.get("wallet", "balance"))))  # Default value in config
            db_session.commit()
            return redirect(url_for("user", username=username))

    elif request.method == "GET":
        return render_template("index.html", form=request.form)

    return render_template("index.html")


@app.route("/user/<username>")
def user(username: str):
    db_user: User = db_session.query(User).filter(User.user_id == username).first()
    wallet = WalletFactory.create_wallet(_config.get("wallet", "type"), db_user)
    return jsonify({"username": username, "balance": wallet.balance})


if __name__ == "__main__":
    app.run(debug=True)
