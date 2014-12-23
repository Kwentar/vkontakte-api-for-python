# Вконтакте API для Python

## Описание

В данном репозитории содержатся модули для работы с [API Вконтакте]
(https://vk.com/dev). 

## Использование

Постим коня на стеночку:

```Python
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
```
В первый раз будет вызван диалог с авторизацией. 

<img src="http://i.gyazo.com/33bc26a85195e6cf16d51f1fb2ff20fb.png">

В случае успешной авторизации, полученный токен будет сохранен в файле 
access_token.txt. В случае необходимости будет выведено окно ввода
капчи.

<img src="http://i.gyazo.com/d11aa303494c299a4b18ad500330af6a.png">

## Требования

Для работы с модулями:

1. Python 2.7.x
2. Requests
3. PyQt4

## Установка Python, библиотек и настройка системы

### Установка Python

Пареходим по [ссылке](https://www.python.org/downloads/) и находим на странице 
большую кнопку "Download Python 2.7.9".

### Установка PyQt4

Переходим по [ссылке](http://www.riverbankcomputing.com/software/pyqt/download).
Находим ссылку на скачивание PyQt4 для Python 2.7 x64 или x32(в зависимости от 
того какой разрядности у вас Windows).

### Установка Requests

Вызываем диалог Выполнить сочетанием клавиш Windows+R. Вбиваем в поле cmd и 
нажимаем Enter. В командной строке набираем:

    pip install requests

Если произошла ошибка, то возможно не настроена переменная окружения PATH.

### Настройка переменной окружения PATH для работы с Python

#### В Windows 8

1. Находим на рабочем столе значок Компьютер, кликаем по нему правой кнопкой и 
выбираем Свойства.
2. Слева в меню выбираем "Дополнительные параметры системы".
3. В открывшемся окне находим кнопку "Переменные среды..." во вкладке 
Дополнительно.
4. Выбираем переменную PATH, нажимаем кнопку "Изменить...".
5. Добавляем в конец строки ";C:\Python27;C:\Python27\Scripts"(без кавычек), 
нажимаем ОК.
