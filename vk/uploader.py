# -*- coding: utf-8 -*-
import requests
import re
import os

class Uploader(object):
    def __init__(self, session=None):
        self.session=session or requests.Session()

    def upload(self, url, files):
        _files={}
        for field, src in files.items():
            if re.match('(?i)https?://', src):
                r=self.session.get(src)
                content=r.content
            else:
                f=open(src, 'rb')
                content=f.read()
                f.close()
            filename=os.path.basename(src)
            _files[field]=(filename, content)
        r=self.session.post(url, files=_files).json()
        if 'error' in r:
            raise UploadError(r['error'])
        return r

class UploadError(Exception):
    pass
