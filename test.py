# -*- coding: utf-8 -*-
from vkclient import *

vk = VkClient()
url = vk.photos.getWallUploadServer()['upload_url']
# Загружать файлы можно по ссылке.
upload_result = vk.upload(url, {'photo': 'http://images4.fanpop.com/image/photos/20500000/Fluttershy-my-little-pony-friendship-is-magic-20524085-570-402.jpg'})
photos = vk.photos.saveWallPhoto(upload_result)
post = vk.wall.post(message="Я люблю разноцветных коней.", attachment="photo{owner_id}_{id}".format(**photos[0]))

# Откроем в стандартном браузере запись.
import webbrowser
webbrowser.open("https://vk.com/wall{}_{}".format(vk.userId, post['post_id']))
