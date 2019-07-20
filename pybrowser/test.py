# coding: utf8
import sys
import asyncio
import pyua
from pybrowser import PyBrowser


url = 'https://blog.csdn.net/xidianbaby/article/details/87790422'

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
