# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from vkapi import Client, ClientError, VkError
from ui.login import Ui_LoginDialog
from ui.captcha import Ui_CaptchaDialog

__all__ = ('VkClient', 'ClientError', 'VkError')

TOKEN_FILE = 'access_token.txt'

class CaptchaDialog(QtGui.QDialog, Ui_CaptchaDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
    def setCaptchaImage(self, imdata):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(imdata)
        self.captchaLabel.setPixmap(pixmap)

class LoginDialog(QtGui.QWidget, Ui_LoginDialog):
    def __init__(self, client):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)  
        self.client = client
        self.loginButton.clicked.connect(self.onLogin)
        
    def onLogin(self):
        username = unicode(self.usernameLine.text())
        password = unicode(self.passwordLine.text())
        self.doLogin(username, password)
        
    def doLogin(self, username, password, captcha_key=None, captcha_sid=None):
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
                print captcha_key
                
                # Если введена капча отправляем запрос еще раз.
                if captcha_key:
                    return self.doLogin(username, 
                                        password, 
                                        captcha_key, 
                                        r['captcha_sid'])
                    
                return
            
            return QtGui.QMessageBox.warning(self,
                                             u"Ошибка авторизации", 
                                             u"<b>Ошибка:</b> {error} - {error_description}".format(**r))
        
        # Закрываем диалог.
        self.close()
        self.client.accessToken = r['access_token']
        self.client.userId = r['user_id']    
        open(self.client.tokenFile, 'w').write(self.client.accessToken)

class VkClient(Client):
    # По умолчанию используем client_id и client_secret от официального
    # приложения для iphone.
    def __init__(self, clientId=3140623, clientSecret='VeWdmVclDCtn6ihuP1nt', 
                 scope=0, tokenFile=TOKEN_FILE, apiVersion=None, 
                 apiDelay=None):
        Client.__init__(self, None, apiVersion, apiDelay)
        self.http.headers['User-Agent'] = "Mozilla 5.0 (VkClient)"
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.scope = scope
        self.tokenFile = tokenFile
        self.app = QtGui.QApplication.instance() or QtGui.QApplication(sys.argv)
        
        # Пробуем прочитать access_token из файла.
        try:
            self.accessToken = open(self.tokenFile).read()
        except:
            pass
         
        # Проверяем токен(отдельного метода для этого нет).   
        try:
            users = self.users.get()
            # Id в отличие от имени и аватары сменить нельзя.
            self.userId = users[0]['id']
        except VkError:
            self.showLoginDialog()      
        
    def showLoginDialog(self):
        d = LoginDialog(self)
        d.show()
        self.app.exec_()
        
    def solveCaptcha(self, url):
        r = self.http.get(url)
        d = CaptchaDialog()
        d.setCaptchaImage(r.content)
        
        if d.exec_():
            return unicode(d.captchaLine.text())
        
        return False
    
    def captchaHandler(self, error):
        args = dict(error.params)
        args['captcha_key'] = self.solveCaptcha(error.captchaImg)
        args['captcha_sid'] = error.captchaSid
        return self.api(error.method, args)
        
if __name__ == '__main__':
    vk = VkClient()
