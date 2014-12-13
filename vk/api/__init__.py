# -*- coding: utf-8 -*-
from errors import *
import requests

DEFAULT_API_VERSION=5.27

class Api(object):
    def __init__(self, access_token=None, api_version=None, session=None):
        self.access_token=access_token
        self.api_version=api_version or DEFAULT_API_VERSION
        self.session=session or requests.Session()

    def api(self, method, params={}):
        params=dict(params)
        if self.access_token and not ('access_token' in params):
            params['access_token']=self.access_token
        if self.api_version and not ('v' in params):
            params['v']=self.api_version
        u='https://api.vk.com/method/{}'.format(method)
        r=self.session.post(u, data=params).json()
        if 'error' in r:
            code=r['error']['error_code']
            if code == 5:
                raise UserAuthorizationFailed(r['error'])
            elif code == 6:
                raise TooManyRequests(r['error'])
            elif code == 9:
                raise FloodControl(r['error'])
            elif code == 10:
                raise InternalServerError(r['error'])
            elif code == 14:
                return self.handleCaptcha(CaptchaNeeded(r['error']))
            elif code == 15:
                raise AccessDenied(r['error'])
            elif code == 17:
                return self.handleValidation(ValidationRequired(r['error']))
            elif code == 113:
                raise InvalidUserId(r['error'])
            elif code == 200:
                raise AccessToAlbumDenied(r['error'])
            elif code == 201:
                raise AccessToAudioDenied(r['error'])
            elif code == 203:
                raise AccessToGroupDenied(r['error'])
            elif code == 300:
                raise AlbumIsFull(r['error'])
            else:
                raise ApiError(r['error'])
        return r['response']

    def handleCaptcha(self, error):
        # Do smth with error.captcha_img and error.captcha_sid
        # error.params['captcha_sid']=error.captcha_sid
        # error.params['captcha_key']=captcha_key
        # return self.api(error.method, error.params)
        raise error

    def handleValidation(self, error):
        raise error

    def __getattr__(self, name):
        return ApiMethod(self, name)

class ApiMethod(object):
    def __init__(self, client, name):
        self.client=client
        self.name=name

    def __call__(self, *args, **kwargs):
        if len(args):
            kwargs.update(args[0])
        return self.client.api(self.name, kwargs)

    def __getattr__(self, name):
        return ApiMethod(self.client, self.name + '.' + name)

if __name__ == '__main__':
    vk=Api()
    r=vk.users.get(user_id=1)
    print u"#{id} {first_name} {last_name}".format(**r[0])
    raw_input("Press Enter to exit.")
