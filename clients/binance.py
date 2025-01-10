from clients.client import Client

class BinanceClient(Client):
    def __init__(self, last_open_time) -> None:
        super().__init__(
            symbol="BTCUSDT", interval="1m", limit="4"
        )
        self.url = f'https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval={self.interval}&startTime={last_open_time}&limit={self.limit}'
     