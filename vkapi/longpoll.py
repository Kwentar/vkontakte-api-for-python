# -*- coding: utf-8 -*-
# https://vk.com/dev/using_longpoll

__author__ = "Sergey Codobear <tz4678@gmail.com>"
__license__ = "GNU General Public License v. 3"

###############################################################################
#                                                                             #
# Коды событий.                                                               #
#                                                                             #
###############################################################################

# 0,$message_id,0 — удаление сообщения с указанным local_id
MESSAGE_DELETED = 0

# 1,$message_id,$flags — замена флагов сообщения (FLAGS:=$flags)
MESSAGE_FLAGS_REPLACED = 1

# 2,$message_id,$mask[,$user_id] — установка флагов сообщения (FLAGS|=$mask)
MESSAGE_FLAGS_SETTED = 2

# 3,$message_id,$mask[,$user_id] — сброс флагов сообщения (FLAGS&=~$mask)
MESSAGE_FLAGS_RESETED = 3

# 4,$message_id,$flags,$from_id,$timestamp,$subject,$text,$attachments —
# добавление нового сообщения
MESSAGE_ADDED = 4

# 8,-$user_id,$extra — друг $user_id стал онлайн, $extra не равен 0, если в
# mode был передан флаг 64, в младшем байте (остаток от деления на 256) числа
# $extra лежит идентификатор платформы (см. ниже)
FRIEND_ONLINE = 8

# 9,-$user_id,$flags — друг $user_id стал оффлайн ($flags равен 0, если
# пользователь покинул сайт (например, нажал выход) и 1, если оффлайн по
# таймауту (например, статус away))
FRIEND_OFFLINE = 9

# 51,$chat_id,$self — один из параметров (состав, тема) беседы $chat_id были
# изменены. $self - были ли изменения вызваны самим пользователем
CHAT_UPDATED = 51

# 61,$user_id,$flags — пользователь $user_id начал набирать текст в диалоге.
# событие должно приходить раз в ~5 секунд при постоянном наборе текста.
# $flags = 1
PRIVATE_TYPING = 61

# 62,$user_id,$chat_id — пользователь $user_id начал набирать текст в беседе
# $chat_id.
CHAT_TYPING = 62

# 70,$user_id,$call_id — пользователь $user_id совершил звонок имеющий
# идентификатор $call_id.
USER_CALL = 71

# 80,$count,0 — новый счетчик непрочитанных в левом меню стал равен $count.
UNREAD_CHANGED = 80

###############################################################################
#                                                                             #
# Флаги сообщений.                                                            #
#                                                                             #
###############################################################################

UNREAD = 1 # сообщение не прочитано 
OUTBOX = 2 # исходящее сообщение 
REPLIED = 4 # на сообщение был создан ответ 
IMPORTANT = 8 # помеченное сообщение 
CHAT = 16 # сообщение отправлено через чат 
FRIENDS = 32 # сообщение отправлено другом 
SPAM = 64 # сообщение помечено как "Спам" 
DELETED = 128 # сообщение удалено (в корзине) 
FIXED = 256 # сообщение проверено пользователем на спам 
MEDIA = 512 # сообщение содержит медиаконтент

class LongPoll(object):
    def __init__(self, client):
        self.client = client
        self.server = None
        self.key = None
        self.ts = None
        self.running = None
        
    def setUp(self):
        r = self.client.messages.getLongPollServer(use_ssl=1)
        self.server = r['server']
        self.key = r['key']
        self.ts = r['ts']
        
    def start(self):
        if self.running:
            raise RuntimeError("Already started.")
        
        self.setUp()
        self.running = True
        
        while self.running:      
            args = dict(act='a_check', 
                        key=self.key, 
                        ts=self.ts, 
                        wait=25, 
                        mode=2)      
            r = self.client.http.post('https://' + self.server, args).json()
            
            if 'updates' in r:
                self.ts = r['ts']
                self.onData(r['updates'])
                continue
            
            self.setUp()
            
    def stop(self):
        self.running = False
        
    def onData(self, updates):
        """Метод для переопределения."""
        pass