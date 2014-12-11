# -*- coding: utf-8 -*-
import sys
import requests
import datetime
import re
import os

USER_AGENT="VkClient v1.05 (Python {}.{}.{})".format(*sys.version_info[:3])
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

    # https://vk.com/dev/auth_direct
    def authDirect(self, username, password, captcha_sid=0, captcha_key=0):
        params={}
        params['username']=username
        params['password']=password
        params['client_id']=self.client_id
        params['client_secret']=self.client_secret
        params['scope']=self.permissions
        if captcha_sid:
            params['captcha_sid']=captcha_sid
        if captcha_key:
            params['captcha_key']=captcha_key
        params['grant_type']='password'
        params['test_redirect_uri']=1
        r=self.session.post('https://oauth.vk.com/token', data=params).json()
        if 'error' in r:        
            if r['error'] == 'need_captcha':
                captcha_sid=r['captcha_sid']
                captcha_key=self.solveCaptcha(r['captcha_img'])
            elif r['error'] == 'need_validation':
                self.authValidate(r['redirect_uri'])
            else:
                raise VkAuthorizationError("{error}: {error_description}"\
                                           .format(**r))
            return self.authDirect(username, password, captcha_sid,
                                   captcha_key)
        self.access_token=r['access_token']
        self.user_id=r['user_id']

    def authSite(self):
        raise VkClientError("Not implemented yet.")

    def authMobile(self):
        raise VkClientError("Not implemented yet.")

    def authServer(self):
        raise VkClientError("Not implemented yet.")

    def authValidate(self, redirect_uri):
        u"""При авторизации из подозрительного места нужно открыть ссылку в 
        браузере и нажать на кнопку, что легко эмулируется."""
        r=self.session.get(redirect_uri)
        m=re.search(r'/security_check\?[^"]+', r.text)
        if m:
            url='https://oauth.vk.com' + m.group(0)
            r=self.session.get(url)
            if r.url == 'https://oauth.vk.com/blank.html?success=1':
                print "User validation passed."
                return
        raise VkValidationError("User validation failed.")

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
                params['captcha_sid']=error['captcha_sid']
                params['captcha_key']=self.solveCaptcha(error['captcha_img'])
            elif error['error_code'] == 17:
                # Получаем новый access_token.
                self.apiValidate(error['redirect_uri'])
            else:
                raise VkApiError(error['error_code'], error['error_msg'])
            # Отправляем запрос повторно.
            return self.api(method, params)
        return r['response']

    def apiValidate(self, redirect_uri):
        raise VkValidationError("User validation required.")

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

    # <VkClient>.<МЕТОД_API_ВКОНТАКТЕ>(<СЛОВАРЬ_ИЛИ_ИМЕНОВАННЫЕ_АРГУМЕНТЫ>)
    # <VkClient>.users.get(user_id=1)
    # <VkClient>.users.get({'user_id': 1}) 
    # <VkClient>.api('users.get', {'user_id': 1})
    def __getattr__(self, name):
        return VkApiMethod(self, name)

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

class VkAuthorizationError(VkClientError):
    def __init__(self, error, error_description):
        super(VkAuthorizationError, self)\
            .__init__("{} {}".format(error, error_description))
        self.type=error

class VkApiError(VkClientError):
    def __init__(self, error_code, error_msg):
        super(VkApiError, self)\
            .__init__("{} {}".format(error_code, error_msg))
        self.code=error_code

class VkUploadError(VkClientError):
    pass

class VkCaptchaError(VkClientError):
    pass

class VkValidationError(VkClientError):
    pass
    