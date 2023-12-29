"""
There will be flask api for this app
"""
import os
import configparser

import dotenv
from flask import Flask, jsonify, request, url_for, redirect, render_template

from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.wallet.wallet_factory import WalletFactory

_config = configparser.ConfigParser()
_config.read(os.path.join(os.getcwd(), "configuration", "equipment.ini"))


def __check_if_api_works():
    dotenv.load_dotenv(os.path.join(os.getcwd(), "configuration", ".env"))
    # Test API
    if db_session.query(User).filter(User.user_id == os.environ.get("DB_USERNAME")).count() == 0:
        db_session.add(User(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"), float(_config.get("wallet", "balance"))))
        db_session.commit()

    db_user: User = db_session.query(User).filter(User.user_id == os.environ.get("DB_USERNAME"))[0]
    if not db_user.verify_password(os.getenv("DB_PASSWORD")):
        raise ValueError("Incorrect password")

    wallet = WalletFactory.create_wallet(_config.get("wallet", "type"), db_user.user_id, db_user.balance)

    wallet.buy_stock("google", 2.1)
    wallet.sell_stock("google", 2.1)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("Login") == "Login":
            username = request.form.get("username")
            password = request.form.get("password")
            if db_session.query(User).filter(User.user_id == username).count() == 0:
                print(f"There is no user with username: {username}")
                return render_template("index.html")
            db_user: User = db_session.query(User).filter(User.user_id == username)[0]
            if not db_user.verify_password(password):
                print("Wrong password!")
                return render_template("index.html")
            return redirect(url_for("user", username=username))

        if request.form.get("Register") == "Register":
            username = request.form.get("username")
            password = request.form.get("password")
            if not db_session.query(User).filter(User.user_id == username).count() == 0:
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
    db_user: User = db_session.query(User).filter(User.user_id == username)[0]
    wallet = WalletFactory.create_wallet(_config.get("wallet", "type"), db_user)
    return jsonify({"username": username, "balance": wallet.balance})


if __name__ == "__main__":
    app.run(debug=True)
