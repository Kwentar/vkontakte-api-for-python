# -*- coding: utf-8 -*-
class ApiError(Exception):
  def __init__(self, error_params):
    self.code=error_params['error_code']
    self.message=error_params['error_msg']
    # 14 Captcha needed.
    self.captcha_sid=error_params.get('captcha_sid')
    self.captcha_img=error_params.get('captcha_img')
    # 17 Validation required.
    self.redirect_uri=error_params.get('redirect_uri')

    params={
        param['key']: param['value']
            for param in error_params['request_params']
    }

    self.oauth=params.pop('oauth')
    self.method=params.pop('method')
    self.params=params

  def __str__(self):
    return "[{}] {}".format(self.code, self.message)

# Специфические ошибки.
class UserAuthorizationFailed(ApiError):
    """User authorization failed"""
    pass

class TooManyRequests(ApiError):
    """Too many requests per second"""
    pass

class FloodControl(ApiError):
    """Flood control"""
    pass

class InternalServerError(ApiError):
    """Internal server error"""
    pass

class CaptchaNeeded(ApiError):
    """Captcha needed"""
    pass

class AccessDenied(ApiError):
    """Access denied"""
    pass

class ValidationRequired(ApiError):
    """Validation required"""
    pass

class InvalidUserId(ApiError):
    """Invalid user id"""
    pass

class AccessToAlbumDenied(ApiError):
    """Access to album denied"""
    pass

class AccessToAudioDenied(ApiError):
    """Access to audio denied"""
    pass

class AccessToGroupDenied(ApiError):
    """Access to group denied"""
    pass

class AlbumIsFull(ApiError):
    """This album is full"""
    pass
    