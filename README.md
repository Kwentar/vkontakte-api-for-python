# Краткое руководство

## Описание

В данном репозитории содержатся модули для работы с [API Вконтакте]
(https://vk.com/dev). 

## Примеры

Постим геев на стеночку в уютненький контактик.

<code>
# -*- coding: utf-8 -*-
from vk.client import *

# Притворяемся официальным приложением для iPhone.
vk=VkClient(client_id=3140623, client_secret='VeWdmVclDCtn6ihuP1nt')
# Авторизуемся напрямую.
vk.authDirect('+79876543210', 'pass123')
u=vk.photos.getWallUploadServer()['upload_url']
# Файлы можно грузить по ссылке.
r=vk.upload(u, {'photo': 'http://sleek25.blog.pl/files/2014/06/tumblr_mumab5h6GF1qhbwg1o1_500.png'})
r=vk.photos.saveWallPhoto(r)
attachment='photo{owner_id}_{id}'.format(**r[0])
# Постим запись на стену.
vk.wall.post(message=u"\u2764\u2764\u2764", attachments=attachment)
</code>

Заметьте, что к методам API Вконтакте можно обращаться как к свойствам 
экземпляра VkClient.

## Требования

Для работы с модулем нужны:

1. Python 2.7.x
2. Библиотека Requests
3. PyQt

## Установка Python, библиотек и настройка системы

### Установка Python

Пареходим по [ссылке](https://www.python.org/downloads/) и находим на странице 
большую кнопку "Download Python 2.7.9". Скачиваем, устанавливаем.

### Установка PyQt

Переходим по [ссылке](http://www.riverbankcomputing.com/software/pyqt/download).
Находим ссылку на скачивание PyQt4 для Python 2.7 x64 или x32(в отличие от 
того какой разрядности у вас Windows). Устанавливаем.

### Установка Requests

Вызываем диалог "Выполнить" сочетанием клавиш Win+R(Win — это клавишка с 
логотипом Windows). Вбиваем в поле cmd и нажимаем Enter. В командной строке 
набираем:

    pip install requests

Если произошла ошибка, то возможно не настроена переменная окружения PATH.

### Настройка переменной окружения PATH для работы с Python

#### В Windows 8

1. Переместите курсор мыши в правую нижню часть экрана.
2. Выберите Параметры → "Панель Управления".
3. Перейдите в "Панель управления\Система и безопасность\Система"(можно 
скопировать в адресную строку).
4. Слева в меню выбираем "Дополнительные параметры системы".
5. В открывшемся окне находим кнопку "Переменные среды..." во вкладке 
"Дополнительно".
6. Выбираем переменную PATH, нажимаем кнопку "Изменить...".
7. Добавяляем в конец строки ";C:\Python27;C:\Python27\Scripts"(без кавычек), 
нажимаем ОК. Заметьте, что точка с запятой является разделителем путей.

Ну или на рабочем столе найдите значок Компьютер, кликнете по нему правой 
кнопкой мыши. Выберите Свойства, далее переходите к п.4.