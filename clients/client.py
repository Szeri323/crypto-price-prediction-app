import json

class Client:
    def __init__(self, symbol, interval, limit) -> None:
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.url = None
        
    async def req(self, session):
        response = await session.request(method='GET', url=self.url)
        value = await response.text()
        value = json.loads(value)
        return value
        
    def write_to_file(self):
        pass

    def read_from_file(self):
        pass