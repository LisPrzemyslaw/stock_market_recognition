from stock_market_recognition.stock_predict.lstm_stock_predict import LstmStockPredict
from stock_market_recognition.stock_receiver.yahoo_receiver import YahooReceiver
import json
import os

_TICKER_INFO_INDEX = 0
_TICKER_HISTORICAL_DATA_INDEX = 1

PREDICTION_DAYS = [2, 7, 10, 30]
LSTM_UNITS = [10, 30, 50]
DROPOUT = [0.2, 0.4]
EPOCH = [10, 15, 25, 50]
BATCH_SIZE = [16, 32, 64]

STOCK_TICKERS = ["MSFT", "GOOG", "DELL", ]

PARAMETERS_DICT = {
    "prediction_days": PREDICTION_DAYS,
    "lstm_units": LSTM_UNITS,
    "dropout": DROPOUT,
    "epoch": EPOCH,
    "batch_size": BATCH_SIZE,
}

default_prediction_day: int = 7
default_lstm_units: int = 50
default_dropout: float = 0.2
default_epoch: int = 25
default_batch_size: int = 32


def main():
    stock_receiver = YahooReceiver()
    ticker_data = {}
    results = {}
    for ticker in STOCK_TICKERS:
        ticker_data[ticker] = stock_receiver.receive_data(ticker, period="MAX")
        results[ticker] = {}
        for parameter_name, parameter_values in PARAMETERS_DICT.items():
            results[ticker][parameter_name] = {}
            for parameter_value in parameter_values:
                print("=====================================")
                print(f"TICKER: {ticker}, PARAMETER: {parameter_name}, VALUE: {parameter_value}")
                print("=====================================")

                # Set default values
                prediction_days = default_prediction_day
                lstm_units = default_lstm_units
                dropout = default_dropout
                epoch = default_epoch
                batch_size = default_batch_size
                # set parameter value
                globals()[parameter_name] = parameter_value

                stock_predictor = LstmStockPredict(ticker_data[ticker], prediction_days, lstm_units, dropout, epoch, batch_size)
                last_days_close_value = ticker_data[ticker][_TICKER_HISTORICAL_DATA_INDEX]["Close"].values[-prediction_days:]

                try:
                    current_price = ticker_data[ticker][_TICKER_INFO_INDEX]["currentPrice"]
                except KeyError:
                    current_price = ticker_data[ticker][_TICKER_HISTORICAL_DATA_INDEX]["Close"].values[-1:]
                predicted_price = round(stock_predictor.predict(last_days_close_value, True), 2)
                mse = round(stock_predictor.mse, 2)
                mse_scaled = round(stock_predictor.mse_scaled, 2)
                rmse = round(stock_predictor.mse ** 0.5, 2)

                results[ticker][parameter_name][parameter_value] = {}
                results[ticker][parameter_name][parameter_value]["predicted_price"] = float(predicted_price)
                results[ticker][parameter_name][parameter_value]["current_price"] = float(current_price)
                results[ticker][parameter_name][parameter_value]["mse"] = float(mse)
                results[ticker][parameter_name][parameter_value]["mse_scaled"] = float(mse_scaled)
                results[ticker][parameter_name][parameter_value]["rmse"] = float(rmse)
    with open(os.path.join(os.getcwd(), "results.json"), "w") as file:
        json.dump(results, file, indent=4)


if __name__ == "__main__":
    main()
