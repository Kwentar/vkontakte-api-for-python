# -*- coding: utf-8 -*-
# https://vk.com/dev/using_longpoll
import threading

"""
Первым параметром каждого события передаётся его код, поддерживаются следующие 
коды событий:  

0,$message_id,0 — удаление сообщения с указанным local_id

1,$message_id,$flags — замена флагов сообщения (FLAGS:=$flags)

2,$message_id,$mask[,$user_id] — установка флагов сообщения (FLAGS|=$mask)

3,$message_id,$mask[,$user_id] — сброс флагов сообщения (FLAGS&=~$mask)

4,$message_id,$flags,$from_id,$timestamp,$subject,$text,$attachments — 
добавление нового сообщения

6,$peer_id,$local_id — прочтение всех входящих сообщений с $peer_id вплоть до 
$local_id включительно

7,$peer_id,$local_id — прочтение всех исходящих сообщений с $peer_id вплоть до
 $local_id включительно

8,-$user_id,$extra — друг $user_id стал онлайн, $extra не равен 0, если в mode 
был передан флаг 64, в младшем байте (остаток от деления на 256) числа $extra 
лежит идентификатор платформы (таблица ниже)

9,-$user_id,$flags — друг $user_id стал оффлайн ($flags равен 0, если 
пользователь покинул сайт (например, нажал выход) и 1, если оффлайн по таймауту 
(например, статус away))

51,$chat_id,$self — один из параметров (состав, тема) беседы $chat_id были 
изменены. $self - были ли изменения вызваны самим пользователем

61,$user_id,$flags — пользователь $user_id начал набирать текст в диалоге. 
событие должно приходить раз в ~5 секунд при постоянном наборе текста. 
$flags = 1

62,$user_id,$chat_id — пользователь $user_id начал набирать текст в беседе 
$chat_id.

70,$user_id,$call_id — пользователь $user_id совершил звонок имеющий 
идентификатор $call_id.

80,$count,0 — новый счетчик непрочитанных в левом меню стал равен $count.
"""

# Каждое сообщение имеет флаг - значение, полученное суммированием любых из 
# следующих параметров.  
UNREAD=1 # сообщение не прочитано 
OUTBOX=2 # исходящее сообщение 
REPLIED=4 # на сообщение был создан ответ 
IMPORTANT=8 # помеченное сообщение 
CHAT=16 # сообщение отправлено через чат 
FRIENDS=32 # сообщение отправлено другом 
SPAM=64 # сообщение помечено как "Спам" 
DELETED=128 # сообщение удалено (в корзине) 
FIXED=256 # сообщение проверено пользователем на спам 
MEDIA=512 # сообщение содержит медиаконтент

"""
Прикрепления
Если в mode был передан флаг 2, то вместе с текстом и заголовком сообщения, 
может быть передан JSON объект содержащий прикрепления, а также другие полезные
 поля. Ниже приведено описание полей этого объекта.  

attach{$i}_type photo, video, audio, doc, wall  тип $i-го прикрепления, где 
i > 0

attach{$i}  {$owner_id}_{$item_id}  идентификатор $i-го прикрепления, где i > 0

fwd {$user_id}_{$msg_id},{$user_id}_{$msg2_id},...  идентификаторы 
прикреплённых сообщений

from    {$user_id}  идентификатор реального автора сообщения если сообщение 
получено из беседы 

Платформы
Если в mode был передан флаг 64, то в событиях с кодом 8 (друг стал онлайн) в 
третьем поле будут возвращаться дополнительные данные $extra, из которых можно 
получить идентификатор платформы $platform_id = $extra & 0xFF 
( = $extra % 256), с которой пользователь вышел в сеть. Этот идентификатор 
можно использовать, например, для отображения того, с мобильного ли устройства 
был обновлен статус онлайн (идентификаторы 1 - 5). 
"""
MOBILE=1 # Мобильная версия сайта или неопознанное мобильное приложение 
IPHONE=2 # Официальное приложение для iPhone 
IPAD=3 # Официальное приложение для iPad 
ANDROID=4 # Официальное приложение для Android 
WPHONE=5 # Официальное приложение для Windows Phone 
WINDOWS=6 # Официальное приложение для Windows 8 
WEB=7 # Полная версия сайта или неопознанное приложение

class LongPoll(object):
    _running=False

    def __init__(self, client, mode=2, wait=25):
        """
        :param VkClient client: экземпляр client.VkClient.
        :param int mode: параметр, определяющий наличие поля прикреплений в 
            получаемых данных с помощью битовой маски. Cумма номеров 
            необходимых опций: 2 - получать прикрепления, 8 - возвращать 
            расширенный набор событий (видеозвонки), 32 - возвращать pts, для 
            работы метода messages.getLongPollHistory без ограничения в 256 
            последних событий, 64 - в событии с кодом 8 (друг стал онлайн) 
            возвращать в третьем поле дополнительные данные (см. описание 
            события 8).
        :param int wait: время удержания ответа сервером.
        """
        self.client=client
        self._mode=mode
        self._wait=wait

    def onUpdateMessages(self, updates, ts, pts):
        print updates, ts, pts

    def start(self):
        if self._running:
            raise LongPollError("Already started.")
        threading.Thread(target=self._start).start()
        self._running=True

    def stop(self):
        self._running=False

    def _start(self):
        self._connect()
        while self._running:
            url=self._getServerUrl()
            r=self.client.session.get(url).json()
            if 'updates' in r:
                self._ts=r['ts']
                self.onUpdateMessages(r['updates'], r['ts'], r.get('pts'))
                continue
            # Соединение потеряно.
            self._connect()

    def _connect(self):
        r=self.client.messages.getLongPollServer(use_ssl=1)
        self._server=r['server']
        self._key=r['key']
        self._ts=r['ts']

    def _getServerUrl(self):   
        url='https://{}?act=a_check&key={}&ts={}&wait={}&mode={}'\
             .format(self._server, self._key, self._ts, self._wait, self._mode)
        return url

class LongPollError(Exception):
    pass
