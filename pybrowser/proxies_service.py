# coding: utf8
import asyncio
import aiohttp
import argparse
from proxybroker import Broker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--addr", help="specify host", 
            default='127.0.0.1')
    parser.add_argument("-p", "--port", help="specify port", 
            default='8808')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    types = ['HTTPS']
    broker = Broker(max_tries=1, loop=loop)
    broker.serve(host=args.addr, port=args.port, types=types, 
            limit=10, max_tries=3)
    loop.run_forever()
    broker.stop()


if __name__ == '__main__':
    main()
