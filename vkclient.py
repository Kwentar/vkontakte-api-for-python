# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from vkapi import VkApi, VkError
from ui.login import Ui_LoginDialog
from ui.captcha import Ui_CaptchaDialog
import os

__author__ = "Sergey Codobear <tz4678@gmail.com>"
__license__ = "GNU General Public License v. 3"
__all__ = ('VkClient', 'VkError')

TOKEN_FILE = 'access_token.txt'
LOGIN_ERROR_TITLE = u"Ощибка авторизации"
LOGIN_ERROR_MESSAGE = u"<b>Ошибка:</b> {error} - {error_description}"

class CaptchaDialog(QtGui.QDialog, Ui_CaptchaDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
    def setCaptchaImage(self, imdata):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(imdata)
        self.captchaLabel.setPixmap(pixmap)

class LoginDialog(QtGui.QDialog, Ui_LoginDialog):
    def __init__(self, client):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)  
        self.client = client
        self.loginButton.clicked.connect(self.onLogin)
        
    def onLogin(self):
        username = unicode(self.usernameLine.text())
        password = unicode(self.passwordLine.text())
        self.login(username, password)
        
    def login(self, username, password, captcha_key=None, captcha_sid=None):
        args = dict(username=username,
                    password=password,
                    client_id=self.client.clientId, 
                    client_secret=self.client.clientSecret,
                    scope=self.client.scope,
                    grant_type='password')

        if captcha_key:
            args['captcha_key'] = captcha_key
            args['captcha_sid'] = captcha_sid

        r = self.client.http.post('https://oauth.vk.com/token', args).json()
        
        if 'error' in r:
            if r['error'] == 'need_captcha':
                captcha_key = self.client.solveCaptcha(r['captcha_img'])
                
                # Если введена капча отправляем запрос еще раз.
                if captcha_key:
                    self.login(username, 
                               password, 
                               captcha_key, 
                               r['captcha_sid'])
            else:         
                QtGui.QMessageBox.warning(self, 
                                          LOGIN_ERROR_TITLE, 
                                          LOGIN_ERROR_MESSAGE.format(**r))
        else:
            self.close()
            self.client.isAuthed = True
            self.client.accessToken = r['access_token']
            self.client.userId = r['user_id']    
            open(self.client.tokenFile, 'w').write(self.client.accessToken)

class VkClient(VkApi):
    # По умолчанию используем client_id и client_secret от официального
    # приложения для iphone.
    def __init__(self, clientId=3140623, clientSecret='VeWdmVclDCtn6ihuP1nt', 
                 scope=0, tokenFile=TOKEN_FILE, accessToken=None, 
                 apiVersion=None, apiDelay=None):
        super(VkClient, self).__init__(accessToken, apiVersion, apiDelay)
        self.http.headers['User-Agent'] = "Mozilla 5.0 (VkClient)"
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.scope = scope
        self.tokenFile = tokenFile
        self.isAuthed = False
        self.app = QtGui.QApplication.instance() or QtGui.QApplication([])
        
        # Пробуем прочитать access_token из файла.
        if self.accessToken is None:
            try:
                self.accessToken = open(self.tokenFile).read()
            except:
                pass
         
        # Проверяем токен(отдельного метода для этого нет).   
        try:
            users = self.users.get()
            # Id в отличие от имени и аватары сменить нельзя.
            self.userId = users[0]['id']
            self.isAuthed = True
        except VkError:
            self.showLoginDialog()      
        
    def showLoginDialog(self):
        d = LoginDialog(self)
        d.exec_()
        
    def solveCaptcha(self, url):
        r = self.http.get(url)
        d = CaptchaDialog()
        d.setCaptchaImage(r.content)
        
        if d.exec_():
            return unicode(d.captchaLine.text())
        
        return False
    
    def captchaHandler(self, error):
        captcha_key = self.solveCaptcha(error.captchaImg)
        
        if captcha_key:
            args = dict(error.params)
            args['captcha_key'] = captcha_key
            args['captcha_sid'] = error.captchaSid
            return self.call(error.method, args)
        
    def logout(self):
        self.isAuthed = False
        self.userId = None
        self.accessToken = None
        
        try:
            os.unlink(self.tokenFile)
        except:
            pass
        
if __name__ == '__main__':
    vk = VkClient()
