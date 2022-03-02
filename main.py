import asyncio
import os

import urllib3
import uvloop

from funcs import renew_connection, reload_target, TorDosya, statistic_info

try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass


async def amain():
    procs = [statistic_info(), renew_connection(int(os.getenv('SOCKS_UPDATE_MIN'))),
             reload_target(int(os.getenv('TAGET_LINK_UPDATE_MIN')))]
    thread_count = int(os.getenv("THREADS_COUNT"))
    print("Запускаю",thread_count,"задач")
    for _ in range(thread_count):
        procs.append(TorDosya().run())
    await asyncio.gather(*procs)


def main():
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())


if __name__ == '__main__':
    main()
