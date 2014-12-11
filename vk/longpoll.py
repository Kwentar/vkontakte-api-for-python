# -*- coding: utf-8 -*-
import threading

class LongPoll(object):
    _thread=None

    def __init__(self, client, mode=2, wait=25):
        self.client=client
        self.mode=mode
        self.wait=wait

    def _connect(self):
        r=self.client.messages.getLongPollServer(use_ssl=1)
        self.server=r['server']
        self.key=r['key']
        self.ts=r['ts']

    def _run(self):
        self._connect()
        while True:
            url='https://{}?act=a_check&key={}&ts={}&wait={}&mode={}'\
                .format(self.server, self.key, self.ts, self.wait, self.mode)
            r=self.client.session.get(url).json()
            if 'updates' in r:
                self.ts=r['ts']
                self.onResponse(r['updates'])
                continue
            self._connect()

    def onResponse(self, updates):
        u"""Do smth."""
        pass
    
    def run(self):
        if not self._thread:
            self._thread=threading.Thread(target=self._run)
            self._thread.start()
