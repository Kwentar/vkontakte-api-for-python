# -*- coding: utf-8 -*-
from api import *
from uploader import *
import requests
import sys

USER_AGENT="vkClient v1.1 (Python {}.{}.{})".format(*sys.version_info[:3])

class Client(Api, Uploader):
    user_id=0

    def __init__(self, client_id, client_secret):
        self.client_id=client_id
        self.client_secret=client_secret
        self.session=requests.Session()
        self.session.headers['User-Agent']=USER_AGENT
        Api.__init__(self, session=self.session)

if __name__ == '__main__':
    vk=Client()
    print vk.users.get(user_id=1)
        
