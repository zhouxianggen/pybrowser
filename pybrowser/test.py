# coding: utf8
import asyncio
import pyua
from pyobject import PyObject
from pybrowser import PyBrowser

log = PyObject().log
url = 'https://weibo.com/u/5404464551?refer_flag=1001030103_'


async def intercept_request(req):
    log.info('request {} {}'.format(req.resourceType, req.url))
    await req.continue_()


async def intercept_response(res):
    log.info('response')


async def test():
    async with PyBrowser() as b:
        page = await b.newPage()
        await page.evaluate("""
            () =>{
                Object.defineProperties(navigator,{
                    webdriver:{
                    get: () => false
                    }
                })
            }
        """)
        await page.setJavaScriptEnabled(enabled=True)
        await page.setUserAgent(pyua.CHROME)
        await page.setRequestInterception(True)
        page.on('request', intercept_request)
        page.on('response', intercept_response)
        
        log.info('goto url')
        await page.goto(url, timeout=30000)
        cookies = await page.cookies()
        log.info('cookies: {}'.format(cookies))
        await asyncio.sleep(30)

asyncio.run(test())
