from abc import ABC, abstractmethod


class StockReceiverInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def receive_data(self, stock_name: str) -> pd.DataFrame:
        """
        This method will return the stock market due to given name and properties

        :param stock_name: name of the stock

        :return: dataframe with all data
        """
        pass
