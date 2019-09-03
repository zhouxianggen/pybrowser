# coding: utf8 
""" 提供模拟浏览器环境 
"""
from __future__ import absolute_import, unicode_literals
import signal
import psutil
import pyppeteer
import pyua
from mayi_proxies import mayi
from pyobject import PyObject


class PyBrowser(PyObject):
    def __init__(self, proxy_server=None):
        PyObject.__init__(self)
        self.proxy_server = proxy_server
        self.browser = None
        self.pid = None


    async def __aenter__(self):
        await self.launch()
        return self.browser

    
    async def __aexit__(self, exc_type, exc, tb):
        self.log.info('close browser')
        await self.browser.close()
        self.force_close()


    async def launch(self):
        self.log.info('launch browser')
        args = [ 
                '--disable-extensions',
                '--hide-scrollbars',
                '--disable-bundled-ppapi-flash',
                '--mute-audio',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-gpu']
        if self.proxy_server:
            args.append('--proxy-server={}'.format(self.proxy_server))
        self.browser = await pyppeteer.launch({
            'headless': False, 
            'devtools': True,
            'args': args,
            'dumpio': True, 
            'ignoreHTTPSErrors': True, 
            'handleSIGHUP': False, 
            'autoClose': False
        })
        self.pid = self.browser.process.pid
        self.log.info('browser launched [{}][{}]'.format(
                self.browser.process.pid, self.browser.wsEndpoint))



    def force_close(self):
        try:
            parent = psutil.Process(self.pid)
            # todo: check if is a chrome process
        except psutil.NoSuchProcess:
            return
        self.log.info('force close browser')
        sig = signal.SIGTERM
        children = parent.children(recursive=True)
        for c in children:
            c.send_signal(sig)
        parent.send_signal(sig)

