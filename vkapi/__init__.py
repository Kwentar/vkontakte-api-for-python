# -*- coding: utf-8 -*-
import os
import re
import time
import requests
import urlparse

__author__ = "Sergey Codobear <tz4678@gmail.com>"
__license__ = "GNU General Public License v. 3"
__all__ = ('VkApi', 'VkError')

DEFAULT_API_VERSION = 5.27
DEFAULT_API_DELAY = 0.34

class VkApi(object):
    """Класс для работы с API Вконтакте. Работает с версией API > 3.
        
    Методы API Вконтакте можно вызывать в удобном виде:
    
        <object VkApi>.users.get(user_id=123)
        
    Вместо именованных аргументов можно первым аргументом передавать словарь:
    
        <object VkApi>.users.get({'user_id': 123})
        
    Это аналогично такой записи:
    
        <object VkApi>.call('users.get', {'user_id': 123})
        
    Список методов API Внонтакте находится здесь <http://vk.com/dev/methods>.
    """   
    def __init__(self, accessToken=None, apiVersion=None, apiDelay=None):
        """Конструктор.
        
        :param accessToken: Токен полученный при авторизации.
        
        :param apiVersion: Версия API Вконтакте. Об актуальной версии можно 
            узнать тут <http://vk.com/dev>.
            
        :param apiDelay: Принудительная задержка возвращения результата 
            выполения метода API. Для приложений есть лимиты обращения к API 
            <http://vk.com/dev/api_requests>. При их превышении будет 
            сгенерирована ошибка.
        """
        self.accessToken = accessToken
        
        self.apiVersion = apiVersion
        
        if self.apiVersion is None:
            self.apiVersion = DEFAULT_API_VERSION
        
        self.apiDelay = apiDelay
        
        if self.apiDelay is None:
            self.apiDelay = DEFAULT_API_DELAY
        
        self.http = requests.session()

    def call(self, method, params=None):
        """Отправляет запрос к API.
        
        :param method: Имя метода.
        :param params: - словарь, необязательный. Параметры запроса.
        :return: Значение поля `response`.
        """
        params = dict(params) or {}

        if self.accessToken and not 'access_token' in params:
            params['access_token'] = self.accessToken

        if self.apiVersion and not 'v' in params:
            params['v'] = self.apiVersion
            
        if self.apiDelay:
            time.sleep(self.apiDelay)
          
        # При вызове метода происходит перенапрвление с помощью mod_rewrite на 
        # какой-то скрипт. 
        # https://api.vk.com/method/users.get?method=wall.post&message=test 
        url = 'https://api.vk.com/method/{}'.format(method)
        r = self.http.post(url, params).json()
        
        if 'error' in r:
            error = VkError(r['error'])
            
            if error.code == 14:
                return self.captchaHandler(error)
            elif error.code == 17:
                return self.validationHandler(error)
            
            raise error
            
        return r['response']
    
    def execute(self, code, **params):
        params['code'] = code
        return self.call('execute', params)

    def captchaHandler(self, error):
        raise error

    def validationHandler(self, error):
        raise error

    def upload(self, upload_url, files):
        """Загружает файлы на сервер.
         
        :param upload_url: Адрес сервера для загрузки файлов.
        :param files: Словарь, где "имя поля" => "путь до файла"(может быть 
            ссылкой). Так же можно передавать кортеж или список вида 
            ("имя файла", "содержимое"). На сервере проверяется расширение 
            файла, mime тип не учитывается(поэтому клиентом он не передается). 
            Проверяются сигнатуры файлов 
            <http://en.wikipedia.org/wiki/List_of_file_signatures> при 
            загрузке изображений. 
        """
        files = dict(files)

        for key, value in files.iteritems():
            if not isinstance(value, basestring):
                continue
            
            filename = value
            
            if re.match('(?i)https?://', filename):
                content = self.http.get(filename).content
                # http://example.com/path/to/file?query -> path/to/file
                filename = urlparse.urlparse(filename).path
            else:
                content = open(filename, 'rb').read()

            # path/to/file -> file
            filename = os.path.basename(filename)
            files[key] = (filename, content)
            
        r = self.http.post(upload_url, files=files).json()
        return r
    
    def uploadWallPhoto(self, photo, group_id=None):
        """Метод для тестирования загрузки фото на стену."""
        args = {'group_id': group_id} if group_id else {} 
        upload_url = self.photos.getWallUploadServer(args)['upload_url']
        upload_result = self.upload(upload_url, {'photo': photo})
        photos = self.photos.saveWallPhoto(upload_result)
        # attachment = "photo{owner_id}_{id}".format(**photos[0])
        # return attachment
        return photos
    
    # Комплексные методы вида <namespace>.<method>.
    def __getattr__(self, name):
        if re.match('[a-z]+$', name):
            return ComplexMethod(self, name) 
    
class ComplexMethod(object):
    def __init__(self, api, prefix):
        self._api = api
        self._prefix = prefix
        
    def __getattr__(self, name):
        def wrapper(*arg, **kw):
            if len(arg) == 1 and isinstance(arg[0], dict):
                dict.update(arg[0], kw)
                kw = arg[0]
                
            return self._api.call(self._prefix + '.' + name, kw)
        
        # Имена методов должны быть в camelCase. 
        if re.match('[a-z]+([A-Z][a-z]+)*$', name):
            return wrapper
        
class VkError(Exception):
    def __init__(self, details):
        Exception.__init__(self)
        self.code = details['error_code']
        self.message = details['error_msg']
        # Параметры капчи.
        self.captchaSid = details.get('captcha_sid')
        self.captchaImg = details.get('captcha_img')
        # redirect_uri для валидации.
        self.redirectUri = details.get('redirect_uri')
        params = {param['key']: param['value'] 
                  for param in details['request_params']}
        self.oauth = params.pop('oauth')
        self.method = params.pop('method')
        self.params = params
    
    def __str__(self):
        return "[{}] {}".format(self.code, self.message)