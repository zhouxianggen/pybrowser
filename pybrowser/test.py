# coding: utf8
import sys
import asyncio
import requests
import pyua
from mayi_proxies import mayi
from pybrowser import PyBrowser

url = 'https://weibo.com/u/5404464551?refer_flag=1001030103_'

async def intercept_request(req):
    print('request')
    print(req)
    print(req.url)
    print(req.headers)
    print(req.postData)
    await req.continue_()

async def intercept_response(res):
    print('response')
    print(res)

async def foo():
    async with PyBrowser(proxy_server=mayi.proxies['http']) as b:
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
        await page.setExtraHTTPHeaders(mayi.headers)
        await page.setUserAgent(pyua.CHROME)
        await page.setRequestInterception(True)
        page.on('request', intercept_request)
        #page.on('response', intercept_response)
        
        print('goto url')
        await page.goto(url, timeout=30000)
        cookies = await page.cookies()
        print('cookies')
        print(cookies)
        #print('wait for selector')
        #e = await page.J('#post-397075827 > dl > dt')
        #print(e)
        print('save')
        await page.screenshot({'path': '/data/share/foo.png'})
        content = await page.content()
        open('content', 'w').write(content)

asyncio.run(foo())
