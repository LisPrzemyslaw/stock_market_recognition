"""
There will be flask api for this app
"""
import os
import configparser

from flask import Flask, jsonify, request, url_for, redirect, render_template, make_response

from stock_market_recognition.database.auth_token import AuthTokenContainer
from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.stock_receiver.stock_receiver_factory import StockReceiverFactory
from stock_market_recognition.stock_predict.stock_predict_factory import StockPredictFactory
from stock_market_recognition.wallet.wallet_factory import WalletFactory
_config = configparser.ConfigParser()
_config.read(os.path.join(os.getcwd(), "configuration", "equipment.ini"))

"""Flask app"""
app = Flask(__name__)

"""Init components"""
StockReceiverFactory.create_stock_receiver(_config.get("stock_receiver", "type"))

"""Constants but variables :)"""
STOCK_PREDICTORS = {}

"""Constants"""
AUTH_KEY = 'auth_token'
PREDICTION_DAYS = 7
STOCK_TICKERS = ["MSFT", "GOOG", "SI", "DELL", "AAPL", "TSLA", "AMZN", "FB", "TWTR", "NFLX", "INTC", "AMD", "NVDA", "IBM", "ORCL",]
current_stock_ticker = STOCK_TICKERS[0]
current_price = ""
predicted_price = ""
recommendation = ""
_TICKER_INFO_INDEX = 0
_TICKER_HISTORICAL_DATA_INDEX = 1


def _update_stock_tickers():
    global STOCK_TICKERS
    STOCK_TICKERS = [stock_ticker for stock_ticker in STOCK_TICKERS if stock_ticker != current_stock_ticker]
    STOCK_TICKERS.insert(0, current_stock_ticker)

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

            response = make_response(redirect(url_for("user", username=username)))
            response.set_cookie(AUTH_KEY, AuthTokenContainer.add_token(db_user.user_id), httponly=True, secure=True, samesite='Lax')
            """
            TODO move it into documentation
            HttpOnly - Zapobiega dostępowi do wartości cookie przez JavaScript po stronie klienta, co minimalizuje ryzyko ataków XSS (Cross-Site Scripting).
            Secure - Wymusza przesyłanie cookie tylko przez bezpieczne połączenie (HTTPS), co chroni przed przechwyceniem tokenu przez ataki typu man-in-the-middle.
            SameSite - Ogranicza wysyłanie cookie do żądań pochodzących z tego samego źródła, co może pomóc w ochronie przed atakami CSRF (Cross-Site Request Forgery).
            """
            return response

        if request.form.get("Register") == "Register":
            username = request.form.get("username")
            password = request.form.get("password")
            if db_session.query(User).filter(User.user_id == username).first():
                print("USER EXIST!")
                return render_template("index.html")
            db_user: User = User(username, password, float(_config.get("wallet", "balance")))  # Default value in config
            db_session.add(db_user)
            db_session.commit()

            response = make_response(redirect(url_for("user", username=username)))
            response.set_cookie(AUTH_KEY, AuthTokenContainer.add_token(db_user.user_id), httponly=True, secure=True, samesite='Lax')
            return response

    if request.method == "GET":
        return render_template("index.html", form=request.form)
    return render_template("index.html")


@app.route("/user/<username>", methods=["GET", "POST"])
def user(username: str):
    global current_stock_ticker, current_price, predicted_price

    db_user: User = db_session.query(User).filter(User.user_id == username).first()
    token = request.cookies.get(AUTH_KEY, None)
    if not AuthTokenContainer.is_user_auth(db_user.user_id, token):
        print("Not authorized!")
        return redirect(url_for("index"))

    wallet = WalletFactory.create_wallet(_config.get("wallet", "type"), db_user)

    if request.method == "POST":
        if request.form.get("Buy") == "Buy":
            amount = float(request.form.get("amount"))
            wallet.buy_stock(current_stock_ticker, amount)
            _update_stock_tickers()
            return render_template(
                "user.html",
                username=username,
                balance=wallet.balance,
                stock_tickers=STOCK_TICKERS,
                current_price=current_price,
                predicted_price=predicted_price,
                recommendation=recommendation)
        if request.form.get("Sell") == "Sell":
            amount = float(request.form.get("amount"))
            wallet.sell_stock(current_stock_ticker, amount)
            _update_stock_tickers()
            return render_template(
                "user.html",
                username=username,
                balance=wallet.balance,
                stock_tickers=STOCK_TICKERS,
                current_price=current_price,
                predicted_price=predicted_price,
                recommendation=recommendation)
        if request.form.get("submit_stock_ticker") == "Select":
            current_stock_ticker = request.form["stocks"]
            _update_stock_tickers()
            stock_receiver = StockReceiverFactory.get_stock_receiver()
            data = stock_receiver.receive_data(current_stock_ticker, period=_config.get("stock_receiver", "period"))
            try:
                current_price = data[_TICKER_INFO_INDEX]["currentPrice"]
            except KeyError:
                current_price = data[_TICKER_HISTORICAL_DATA_INDEX]["Close"].values[-1:]  # TODO

            STOCK_PREDICTORS[current_stock_ticker] = StockPredictFactory.create_stock_predict(_config.get("stock_predict", "type"), data, PREDICTION_DAYS)
            last_days_close_value = data[_TICKER_HISTORICAL_DATA_INDEX]["Close"].values[-PREDICTION_DAYS:]
            predicted_price = round(STOCK_PREDICTORS[current_stock_ticker].predict(last_days_close_value), 2)
            # TODO update the recommendation
            return render_template(
                "user.html",
                username=username,
                balance=wallet.balance,
                stock_tickers=STOCK_TICKERS,
                current_price=current_price,
                predicted_price=predicted_price,
                recommendation=recommendation)

    if request.method == "GET":
        return render_template(
            "user.html",
            username=username,
            balance=wallet.balance,
            stock_tickers=STOCK_TICKERS,
            current_price=current_price,
            predicted_price=predicted_price,
            recommendation=recommendation)
    return render_template(
        "user.html", username=username, balance=wallet.balance, stock_tickers=STOCK_TICKERS, current_price=current_price, predicted_price=predicted_price, recommendation=recommendation)


if __name__ == "__main__":
    app.run(debug=True)
