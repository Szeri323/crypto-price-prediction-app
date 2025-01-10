import asyncio
import aiohttp
import logging
import sys
import os
from dotenv import load_dotenv


from db_scripts.db_config import Database

from clients.binance import BinanceClient
from clients.bitfinex import BitfinexClient
from clients.bybit import BybitClient
from clients.kraken import KrakenClient

async def main():
    load_dotenv()
    db = Database(os.environ.get('USER'), os.environ.get('PASSWORD'), os.environ.get('DATABASE'))
    await db.connect()
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Hello from logging.')
    print("Hello world!")
    records = await db.select_modifier_from('MAX', 'open_time', 'b_d_t')
    record = records[0]
    open_time = record['max'] + 60000
    if open_time == None:
        open_time = 0
    print(open_time)
    binance = BinanceClient(open_time)
    bybit = BybitClient()
    bitfinex = BitfinexClient()
    kraken = KrakenClient()
    
    async with aiohttp.ClientSession() as session:
        data_binance = await binance.req(session)
        for data in data_binance:
            # last value is ignored
            open_time, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume = data[:-1]
            await db.insert_into("b_d_t", ['open_time', 'close_time'], (open_time,close_time))
        await db.close()

if __name__ == '__main__':
    asyncio.run(main())