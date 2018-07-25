import requests
from bs4 import BeautifulSoup
import re
import json


class autoLogin:
    def __init__(self , email , pwd):
        self.email = email
        self.pwd = pwd

        self.session = requests.session()
        self.expireDay = ''
        self.currentMoney = 0
        self.state = ''
        
    def initSession(self):

        loginPage = self.session
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
        
        try:
            loginPage = loginPage.get('http://okav.com.tw/do.php?act=login' , headers=headers)
            return loginPage.text
        except:
            raise Exception('Connect Failed')

    def login(self):

        loginPage = self.initSession()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
        data = {
            'url' : 'http://okav.com.tw/',
            'user_email' : self.email,
            'user_passwd' : self.pwd
            }
        logger = self.session

        try:
            logger = logger.post('http://okav.com.tw/do.php?act=login' , headers=headers , data=data)

            soup = BeautifulSoup(logger.text , 'html.parser')

            if soup.find('p' , {'class':'lost'}):
               raise Exception('ID incorrect')
            return
        except:
            raise Exception('Connect Failed')

    def sign(self):

        dashboardPage = self.session

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }

        def sendSignReq():
            signer = self.session

            try:
                signer = signer.post('http://okav.com.tw/modules.php' , data={'day':'up'} , headers=headers)

                if re.search('skin/okav_tw/images/A00[1-2].jpg', signer.text).group(0).split('/')[-1] == 'A002.jpg':
                    return signer.text
                else:
                    return False

            except:
                raise Exception('Connect Failed')
                
        try:
            dashboardPage = dashboardPage.get('http://okav.com.tw/modules.php' , headers=headers).text


            signImg = re.search('skin/okav_tw/images/A00[1-2].jpg', dashboardPage).group(0).split('/')[-1]

            isSigned = False
            
            if signImg == 'A001.jpg':
                afterSinged = sendSignReq()
                if afterSinged:
                    dashboardPage = afterSinged
                    isSigned = True
                    self.state = 'Signed Success'
            elif signImg == 'A002.jpg':
                isSigned = True
                self.state = 'Already Signed'

            if isSigned:
                soup = BeautifulSoup(dashboardPage , 'html.parser')
                topInfo = soup.find('div' , {'class' : 'topInfo'})
                normal = topInfo.find('p' , {'class' : 'normal'})

                self.currentMoney = re.search('[0-9]+' , normal.find('font').contents[0]).group(0)
                self.expireDay = re.search('[0-9]+\-[0-9]+\-[0-9]+' , normal.find('font').contents[1].text).group(0)
                return
            else:
                self.state = 'Error happened'
                return "Error happened"
        except:
            raise Exception('Connect Failed')
        
    def getMessage(self):
        return {
            'usr' : self.email,
            'state' : self.state,
            'current fund' : self.currentMoney,
            'Expire Day' : self.expireDay
            }
        
        
            
def main():
    t = autoLogin("" , "")
    t.login()
    t.sign()
    print(t.getMessage())

if __name__ == '__main__':
    main()
    
