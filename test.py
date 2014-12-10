# -*- coding: utf-8 -*-
from vkapi import *

vk=VkApi()
vk.authDirect('<EMAIL_ИЛИ_ТЕЛЕФОН>', '<ПАРОЛЬ>', 3140623, 'VeWdmVclDCtn6ihuP1nt')
# К методам API Вконтакте можно обращаться как к атрибутам экземпляра класса VkApi.
u=vk.photos.getWallUploadServer()['upload_url']
# Можно загружать файлы по ссылке.
r=vk.upload(u, {'photo': 'http://sleek25.blog.pl/files/2014/06/tumblr_mumab5h6GF1qhbwg1o1_500.png'})
r=vk.photos.saveWallPhoto(r)
attachment='photo{owner_id}_{id}'.format(**r[0])
vk.wall.post(message=u"\u2764\u2764\u2764", attachments=attachment)
