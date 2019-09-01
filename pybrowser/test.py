# coding: utf8
import sys
import asyncio
import requests
import pyua
from mayi_proxies import mayi
from pybrowser import PyBrowser

url = 'https://www.baidu.com/'
#r = requests.get(url, proxies=mayi.proxies, headers=mayi.headers)
r = requests.get(url, proxies={"https": "http://127.0.0.1:8808", 
        "http": "http://127.0.0.1:8808"})
print(r.status_code, len(r.content))

"""
async def foo():
    async with PyBrowser() as b:
        print('open url')
        page = await b.newPage()
        await page.setUserAgent(pyua.CHROME)
        await page.goto(url, timeout=5000)
        await page.screenshot({'path': '/data/share/foo.png'})
        content = await page.content()
        open('content', 'w').write(content)

asyncio.run(foo())
"""
