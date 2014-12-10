# -*- coding: utf-8 -*-
from vk.client import *

vk=VkClient(client_id=3140623, client_secret='VeWdmVclDCtn6ihuP1nt')
vk.authDirect('Login', 'Password')
u=vk.photos.getWallUploadServer()['upload_url']
r=vk.upload(u, {'photo': 'http://sleek25.blog.pl/files/2014/06/tumblr_mumab5h6GF1qhbwg1o1_500.png'})
r=vk.photos.saveWallPhoto(r)
attachment='photo{owner_id}_{id}'.format(**r[0])
vk.wall.post(message=u"\u2764\u2764\u2764", attachments=attachment)
