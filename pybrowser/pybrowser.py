# coding: utf8 
""" 提供模拟浏览器环境 
"""
import signal
import time
import asyncio
import pyua
import psutil
import pyppeteer
from pyobject import PyObject


class BrowserContext(PyObject):
    def __init__(self, proxy_server=None):
        PyObject.__init__(self)
        self.name = ''
        self.browser = None
        self.connected = None
        self.proxy_server = proxy_server
        self.deadline = 0


    async def recheck(self):
        pages = await self.browser.pages()
        if len(pages) == 1 and pages[0].url == 'about:blank':
            self.deadline = 0


    async def get_browser(self):
        if not self.browser or not self.connected:
            await self.reset()
            return None
        if self.deadline:
            if self.deadline < time.time():
                await self.reset()
            return None
        pages = await self.browser.pages()
        self.log.info('[{}] current pages'.format(self.name))
        for idx,p in enumerate(pages):
            self.log.info('\t[{}:{}:{}]'.format(idx, p.isClosed(), p.url))
        if len(pages) == 1 and pages[0].url == 'about:blank':
            return self.browser
        await self.reset()
        return None


    async def reset(self):
        self.log.info('reset')
        if self.browser:
            self.suicide()
            #await self.close_browser()
        while not self.connected:
            await self.launch_browser()
        

    async def launch_browser(self):
        self.log.info('launch browser')
        args = ['--no-sandbox']
        if self.proxy_server:
            args.append('--proxy-server={}'.format(self.proxy_server))
        self.browser = await pyppeteer.launch(args=args, 
                ignoreHTTPSErrors=True, handleSIGHUP=False, autoClose=False)
        self.log.info('browser launched on [{}][{}]'.format(
                self.browser.process.pid, self.browser.wsEndpoint))
        self.name = str(self.browser.process.pid)
        self.connected = True
        self.deadline = 0

    
    def on_disconnected(self):
        self.log.warning('Disconnected')
        self.connected = False


    async def close_browser(self):
        self.log.info('close current browser [{}][{}]'.format(
                self.browser.process.pid, self.browser.wsEndpoint))
        await self.browser.close()
        self.name = ''
        self.browser = None
        self.connected = False
        self.deadline = 0


    def suicide(self):
        sig = signal.SIGTERM
        pid = self.browser.process.pid
        self.log.info('suicide [{}]'.format(pid))
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for c in children:
                c.send_signal(sig)
            parent.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
        self.name = ''
        self.browser = None
        self.connected = False
        self.deadline = 0


class BrowserPool(PyObject):
    def __init__(self, pool_size=5, proxy_server=None):
        PyObject.__init__(self)
        self.pool = [BrowserContext(proxy_server) for i in range(pool_size)]


    async def get_browser_context(self, deadline=5):
        self.log.info('get browser context')
        for ctx in self.pool:
            self.log.info('check [{}]'.format(ctx.name))
            browser = await ctx.get_browser()
            if browser is not None:
                self.log.info('get [{}]'.format(ctx.name))
                ctx.daedline = deadline
                return ctx
        return None
    
