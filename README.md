pybrowser
![](https://img.shields.io/badge/python%20-%203.7-brightgreen.svg)
========
> python 提供模拟浏览器环境 

## `Install`

+ Install
`pip3.7 install -r requirements.txt`

+ Linux 下安装依赖
`yum install pango.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXext.x86_64 libXi.x86_64 libXtst.x86_64 cups-libs.x86_64 libXScrnSaver.x86_64 libXrandr.x86_64 GConf2.x86_64 alsa-lib.x86_64 atk.x86_64 gtk3.x86_64 ipa-gothic-fonts xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc -y'


## Sample
``` python
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
```

