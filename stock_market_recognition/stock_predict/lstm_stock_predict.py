from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface
from sklearn.preprocessing import MinMaxScaler


class LstmStockPredict(StockPredictInterface):
    def __init__(self, data: tuple[dict, pd.DataFrame]):
        super().__init__(data)

    def predict(self) -> str:
        """
        This function will predict if the stock market is ready to buy

        :return: string "BUY", "SELL", or "WAIT"
        """
        pass

    def _scale_data(self):
        """
        This function will scale the data to be between 0 and 1

        :return: scaled data
        """
        scaler = MinMaxScaler(feature_range=(0, 1))
        # TODO finish this function

    def fit(self):
        """
        This function will fit the data to the model
        """
        pass
