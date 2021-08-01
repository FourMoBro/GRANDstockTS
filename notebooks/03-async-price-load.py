#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import requests
import datetime, time
import aiohttp, asyncpg, asyncio
from dotenv import load_dotenv, find_dotenv


# In[ ]:


load_dotenv(find_dotenv())
api_key2 = os.environ.get("POLYGON_API_KEY")
host2 = os.environ.get("DB_HOST")
database2 = os.environ.get("DB_NAME")
user2 = os.environ.get("DB_USER")
password2 = os.environ.get("DB_PASSWORD")


# In[ ]:


async def write_to_db(connection, params):
    await connection.copy_records_to_table('stock_price_temp', records=params)


# In[ ]:


async def get_price(pool, stock_id, url):
    try: 
        async with pool.acquire() as connection:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    resp = await response.read()
                    response = json.loads(resp)
                    params = [(stock_id, datetime.datetime.fromtimestamp(bar['t'] / 1000.0), round(bar['o'], 2), round(bar['h'], 2), round(bar['l'], 2), round(bar['c'], 2), bar['v']) for bar in response['results']]
                    await write_to_db(connection, params)

    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


# In[ ]:


async def get_prices(pool, symbol_urls):
    try:
        # schedule aiohttp requests to run concurrently for all symbols
        ret = await asyncio.gather(*[get_price(pool, stock_id, symbol_urls[stock_id]) for stock_id in symbol_urls])
        print("Finalized all. Returned  list of {} outputs.".format(len(ret)))
    except Exception as e:
        print(e)


# In[ ]:


async def get_stocks():
    # create database connection pool
    pool = await asyncpg.create_pool(user=user2, password=password2, database=database2, host=host2, command_timeout=60)
    
    # get a connection
    async with pool.acquire() as connection:
        stocks = await connection.fetch("SELECT * FROM stocks WHERE id IN (SELECT holding_id FROM holdings_temp)")

        symbol_urls = {}
        for stock in stocks:
            symbol_urls[stock['id']] = f"https://api.polygon.io/v2/aggs/ticker/{stock['symbol']}/range/1/minute/2021-06-01/2021-07-30?adjusted=true&sort=asc&limit=50000&apiKey={api_key2}"

    await get_prices(pool, symbol_urls)


# In[ ]:


start = time.time()


# In[ ]:


asyncio.run(get_stocks())


# In[ ]:


end = time.time()


# In[ ]:


print("Took {} seconds.".format(end - start))


# In[ ]:


api_key2 


# In[ ]:




