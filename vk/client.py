# -*- coding: utf-8 -*-
from api import *
from uploader import *
import requests
import sys

USER_AGENT="vkClient v1.1 (Python {}.{}.{})".format(*sys.version_info[:3])

class Client(Api, Uploader):
    def __init__(self):
        self.session=requests.Session()
        self.session.headers['User-Agent']=USER_AGENT
        # Api.__init__(self, session=self.session)
        self.api_version=DEFAULT_API_VERSION
        self.access_token=None
        self.user_id=0

if __name__ == '__main__':
    vk=Client()
    print vk.users.get(user_id=1)
        
