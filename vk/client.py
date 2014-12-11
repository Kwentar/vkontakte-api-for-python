# -*- coding: utf-8 -*-
import sys
import requests
import datetime
import re
import os

USER_AGENT="VkClient v1.0 (Python {}.{}.{})".format(*sys.version_info[:3])
API_VERSION=5.27

class VkClient(object):
    user_id=0
    expires_at=None
    session=requests.session()
    session.headers['User-Agent']=USER_AGENT

    def __init__(self, client_id=0,  client_secret='', permissions='',\
                 access_token='', api_version=API_VERSION):
        self.client_id=client_id
        self.client_secret=client_secret
        self.permissions=permissions
        self.access_token=access_token
        self.api_version=api_version

    def authRequest(self, url, params):
        params=dict(params)
        r=self.session.post(url, data=params).json()
        if 'error' in r:        
            if r['error'] == 'need_captcha':
                self.addCaptchaParams(params, r)
                return self.authRequest(url, params)
            if r['error'] == 'need_validation':
                return self.validate(r['redirect_uri'])
            raise VkAuthorizationError(r['error'], r['error_description'])
        self.access_token=r['access_token']
        if 'user_id' in r:
            self.user_id=r['user_id']
        if r.get('expires_in') > 0:
            self.expires_at=datetime.datetime.now() +\
                            datetime.timedelta(seconds=r['expires_in'])

    def authDirect(self, username, password):
        params={}
        params['username']=username
        params['password']=password
        params['client_id']=self.client_id
        params['client_secret']=self.client_secret
        params['scope']=self.permissions
        params['grant_type']='password'
        self.authRequest('https://oauth.vk.com/token', params)

    def authSite(self):
        raise VkClientError("Not implemented yet.")

    def authMobile(self):
        raise VkClientError("Not implemented yet.")

    def authServer(self):
        raise VkClientError("Not implemented yet.")

    def isAuth(self):
        u"""Проверяет авторизован ли пользователь."""
        try:
            if self.users.isAppUser():
                return True
        except VkApiError, e:
            pass
        return False

    def api(self, method, params={}):
        params=dict(params)
        params['access_token']=self.access_token
        params['v']=self.api_version
        url='https://api.vk.com/method/{}'.format(method)
        r=self.session.post(url, data=params).json()
        if 'error' in r:
            error=r['error']
            if error['error_code'] == 14:
                self.addCaptchaParams(params, error)
            elif error['error_code'] == 17:
                # Получаем новый access_token.
                self.validate(error['redirect_uri'])
            else:
                raise VkApiError(error['error_code'], error['error_msg'])
            # Отправляем запрос повторно.
            return self.api(method, params)
        return r['response']

    # <VkClient>.<МЕТОД_API_ВКОНТАКТЕ>(<СЛОВАРЬ_ИЛИ_ИМЕНОВАННЫЕ_АРГУМЕНТЫ>)
    # <VkClient>.users.get(user_id=1)
    # <VkClient>.users.get({'user_id': 1}) 
    # <VkClient>.api('users.get', {'user_id': 1})
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
        raise VkCaptchaError("CAPTCHA required.")

    def validate(self, redirect_uri):
        raise VkValidationError("User validation required.")

    def addCaptchaParams(self, request_params, captcha_params):
        request_params['captcha_sid']=captcha_params['captcha_sid']
        captcha_key=self.solveCaptcha(captcha_params['captcha_img'])
        request_params['captcha_key']=captcha_key

class VkApiMethod(object):
    def __init__(self, client, name):
        self.client=client
        self.name=name

    def __call__(self, *args, **kwargs):
        if len(args):
            kwargs.update(args[0])
        return self.client.api(self.name, kwargs)

    def __getattr__(self, name):
        return self.__class__(self.client, self.name + '.' + name)

class VkClientError(Exception):
    pass

class VkCaptchaError(VkClientError):
    pass

class VkValidationError(VkClientError):
    pass

class VkAuthorizationError(VkClientError):
     def __init__(self, error_type, error_description):
        super(VkAuthorizationError, self)\
            .__init__("{}: {}".format(error_type, error_description))
        self.type=error_type

class VkApiError(VkClientError):
    def __init__(self, error_code, error_msg):
        super(VkApiError, self)\
            .__init__("[{}] {}".format(error_code,error_msg))
        self.code=error_code

class VkUploadError(VkClientError):
    pass
    