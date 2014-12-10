# -*- coding: utf-8 -*-
import requests
import re
import os

DEFAULT_API_VERSION=5.27
TOKEN_AUTH_URL='https://oauth.vk.com/token'
API_URL='https://api.vk.com/method/{method}'

class VkApi(object):
    def __init__(self, access_token=None, api_version=DEFAULT_API_VERSION):
        self.access_token=access_token
        self.version=api_version
        self.session=requests.Session()

    def authDirect(self, username, password, client_id, client_secret,\
                   scope=None, captcha_sid=None, captcha_key=None):
        params={}
        params['username']=username
        params['password']=password
        params['client_id']=client_id
        params['client_secret']=client_secret
        if scope != None:
            params['scope']=scope
        if captcha_sid != None:
            params['captcha_sid']=captcha_sid
        if captcha_key != None:
            params['captcha_key']=captcha_key
        params['grant_type']='password'
        r=self.session.post(TOKEN_AUTH_URL, data=params).json()
        if 'error' in r:        
            if r['error'] == 'need_captcha':
                captcha_key=self.solveCaptcha(r['captcha_img'])
                return self.authDirect(username, password, client_id, 
                                       client_secret, scope, captcha_sid,
                                       r['captcha_sid'], captcha_key)
            if r['error'] == 'need_validation':
                return self.validate(r['redirect_uri'])
            raise VkAuthError(r['error'], r['error_description'])
        self.access_token=r['access_token']
        self.user_id=r['user_id']
        self.username=username
        self.password=password
        self.client_id=client_id
        self.client_secret=client_secret
        self.scope=scope

    def authSite(self):
        """Not implemented yet."""
        pass

    def authMobile(self):
        """Not implemented yet."""
        pass

    def authServer(self):
        """Not implemented yet."""
        pass

    def call(self, api_method, params={}):
        params=dict(params)
        if not ('access_token' in params) and self.access_token != None:
            params['access_token']=self.access_token
        if not ('v' in params):
            params['v']=self.version
        url=API_URL.format(method=api_method)
        r=self.session.post(url, data=params).json()
        if 'error' in r:
            error=r['error']
            if error['error_code'] == 14:
                params['captcha_sid']=r['captcha_sid']
                params['captcha_key']=self.solveCaptcha(r['captcha_img'])
                return self.call(api_method, params)
            if error['error_code'] == 17:
                return self.validate(error['redirect_uri'])
            raise VkApiError(error['error_code'], error['error_msg'])
        return r['response']

    # VkApi().<ИМЯ_МЕТОДА_API_ВКОНТАКТЕ>(<СЛОВАРЬ_ЛИБО_ИМЕНОВАННЫЕ_ПАРАМЕТРЫ>)
    # VkApi().users.get(user_id=1)
    # VkApi().users.get({'user_id': 1}) 
    # VkApi().call('users.get', {'user_id': 1})
    def __getattr__(self, name):
        return VkApiMethod(self, name)

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
            # Баг с non-ascii символами в имени файла.
            filename=os.path.basename(src).encode('ascii', 'replace')
            _files[field]=(filename, content)
        r=self.session.post(url, files=_files).json()
        if 'error' in r:
            raise VkUploadError(r['error'])
        return r

    def solveCaptcha(self, image_url):
        raise VkCaptchaError("Captcha needed.")

    def validate(self, redirect_uri):
        raise VkValidationError("Validation needed.")

    def checkAccessToken(self):
        if self.access_token != None:
            try:
                if self.users.isAppUser():
                    return True
            except VkApiError, e:
                pass
        return False

class VkApiMethod(object):
    def __init__(self, api, name):
        self.api=api
        self.name=name

    def __call__(self, *args, **kwargs):
        if len(args):
            kwargs.update(args[0])
        return self.api.call(self.name, kwargs)

    def __getattr__(self, name):
        return self.__class__(self.api, self.name + '.' + name)

class VkError(Exception):
    pass

class VkCaptchaError(VkError):
    pass

class VkValidationError(VkError):
    pass

class VkAuthError(Exception):
     def __init__(self, error_type, error_description):
        super(VkAuthError, self).__init__("{}: {}".format(error_type,\
                                                          error_description))
        self.type=error_type

class VkApiError(VkError):
    def __init__(self, error_code, error_msg):
        super(VkApiError, self).__init__("[{}] {}".format(error_code,\
                                                          error_msg))
        self.code=error_code

class VkUploadError(VkError):
    pass
    