# coding: utf8
import asyncio
import json
import pyua
from pyutil import get_logger
from pybrowser import BrowserPool


log = get_logger()
url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E9%82%B5%E4%B8%9C&ie=utf8&_sug_=n&_sug_type_='
pool = BrowserPool()


async def foo():
    while True:
        c = await pool.get_browser_context()
        if c is not None:
            break
    page = await c.browser.newPage()
    await page.setUserAgent(pyua.CHROME)
    await page.goto(url)
    await page.screenshot({'path': '/data/share/foo.png'})
    await page.waitForXPath('//*[@id="pagebar_container"]/div')
    es = await page.Jx('//*[starts-with(@id, "sogou_vr_11002601_title_")]')
    hrefs = []
    for e in es:
        href = await page.evaluate("e => e.href", e)
        log.info('click [{}]'.format(href))
        await e.click()
        await asyncio.sleep(1)
        pages = await c.browser.pages()
        for idx,p in enumerate(pages):
            log.info('\t[{}:{}:{}]'.format(idx, p.isClosed(), p.url))
        await asyncio.sleep(2)


asyncio.run(foo())
