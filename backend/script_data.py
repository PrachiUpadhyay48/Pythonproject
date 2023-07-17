import pandas as pd
import requests
import psycopg2


class ScriptData:
    def __init__(self, api_key, db_host, db_port, db_name, db_user, db_password):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def fetch_intraday_data(self, script):
        function = "TIME_SERIES_INTRADAY"
        interval = "1min"
        datatype = "json"

        params = {
            "function": function,
            "symbol": script,
            "interval": interval,
            "apikey": self.api_key,
            "datatype": datatype
        }
        
class Strategy:
    def __init__(self, script_name):
        self.script_name = script_name
        self.df = None
        self.close_data = None
        self.indicator_data = None

    def fetch_intraday_historical_data(self):
        script_data = ScriptData(self.api_key, self.db_host, self.db_port, self.db_name, self.db_user, self.db_password)
        self.df = script_data.fetch_intraday_historical_data(self.script_name)
        self.close_data = self.df['close'] if self.df is not None else None

    def compute_indicator_data(self):
        if self.close_data is not None:
            self.indicator_data = indicator1(self.close_data)

    def execute_strategy(self):
        self.fetch_intraday_historical_data()
        self.compute_indicator_data()

# Example usage
strategy = Strategy('AAPL')
strategy.execute_strategy()

# Access the fetched intraday historical data, close_data, and indicator_data
intraday_data = strategy.df
close_data = strategy.close_data
indicator_data = strategy.indicator_data

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception("Error fetching data from Alpha Vantage")

    def convert_intraday_data(self, script):
        intraday_data = self.fetch_intraday_data(script)

        time_series_key = list(intraday_data.keys())[1]
        time_series = intraday_data[time_series_key]

        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.columns = ["open", "high", "low", "close", "volume"]
        df.index = pd.to_datetime(df.index)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(int)

        return df

    def __getitem__(self, key):
        # Define the behavior of the [] operator
        pass

    def __setitem__(self, key, value):
        # Define the behavior of the []= operator
        pass

    def __contains__(self, key):
        # Define the behavior of the 'in' operator
        pass
