# -*- coding: utf-8 -*-
import threading

class LongPoll(object):
    _thread=None

    def __init__(self, client, use_ssl=1, need_pts=1, mode=2, wait=25):
        self.client=client
        self.use_ssl=use_ssl
        self.need_pts=need_pts
        self.mode=mode
        self.wait=wait

    def _connect(self):
        r=self.client.messages.getLongPollServer(use_ssl=self.use_ssl,
                                                 need_pts=self.need_pts)
        self.server=r['server']
        self.key=r['key']
        self.ts=r['ts']

    def _run(self):
        self._connect()
        while True:
            protocol='https' if self.use_ssl else 'http'
            url='{0}://{1}?act=a_check&key={2}&ts={3}&wait={4}&mode={5}'\
                .format(protocol, self.server, self.key, self.ts, self.wait,
                        self.mode)
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
            