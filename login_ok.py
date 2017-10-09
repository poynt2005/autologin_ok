#!/usr/bin/python
#coding:utf-8
import mechanize
import re
import datetime
from mailnotifer_pchome import Notifer_pchome as Notifer

class auto_login(object):
    def __init__(self,email,password , Num = None):
        self.email = email
        self.password = password
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [("User-Agent" , "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")]
        self.Num = None
        if Num:
            self.Num = Num
            
    def login(self):
        self.browser.open('http://okav.com.tw/login.php?url=%2Fmodules.php')
        self.browser.select_form(nr=1)
        self.browser["user_email"] = self.email
        self.browser["user_passwd"] = self.password
        self.browser.submit()
        error_message = u'用戶不存在!請確認您輸入的是Email帳戶或用戶名! '.encode('utf8')
       
        if not re.search(error_message , str(self.browser.response().read())) == None:
            return 1
        else:
            return 0

    def click_button(self):
        key_src = re.compile('src\=\"skin\S+\.jpg\"')
        
        res = self.browser.open("http://okav.com.tw/modules.php")
        res_text = str(res.read())

        pic_temp = key_src.findall(res_text)

        expire_day = ''
        
        pic_url = ""
        for i in pic_temp:
            pic_url = str(i)


        if pic_url == 'src=\"skin/okav_tw/images/A001.jpg\"':
            self.browser.select_form(nr = 1)
            self.browser.submit()
            get_sign_res = self.browser.open('http://okav.com.tw/modules.php')
            
            get_sign_res_text = str(get_sign_res.read())
            pic_temp = key_src.findall(get_sign_res_text)
    
            signed_pic_url = ''
            for i in pic_temp:
                signed_pic_url = str(i)
    
            if signed_pic_url == 'src=\"skin/okav_tw/images/A002.jpg\"':
                #print('Signed Success')
                expire_day = self.get_point(get_sign_res_text , 1)
            else:
                #print('Signed failed')
                self.write_log(0,'', 2)
                expire_day = None
                
        elif pic_url == 'src=\"skin/okav_tw/images/A002.jpg\"':
            #print('already signed')
            
            expire_day = self.get_point(res_text , 3)
        else:
            print('Unknown page , maybe login failed')
            self.write_log(0,'', 0)
            expire_day = None

        return expire_day
            
    def close_browser(self):
       self.browser.close()


    #flag == 1 , not signed yet ; flag == 3 , already signed
    def get_point(self , input_text , flag):
        point_keyword = u'購物金：[0-9]+'.encode('utf8')
        expired_keyword = u'至[0-9]+\-[0-9]+\-[0-9]+'.encode('utf8')
        
        find_str = re.compile(point_keyword)    
        str_tmp = find_str.findall(input_text)  
        point_str = ''
        for i in str_tmp:
            point_str = str(i)

        find_str = re.compile(expired_keyword)    
        str_tmp = find_str.findall(input_text)
        expired_str = ''
        for i in str_tmp:
            expired_str = str(i)

        expired_date = expired_str.split('至')[1]
        point = point_str.split('：')[1]
            
        self.write_log(point , expired_date , flag)
        return expired_date
        

    def write_log(self , input_point , input_expiredate, flag):
        current_time = str(datetime.datetime.now())

        #error
        if flag == 0:
            log = 'Log time : %s\nMessage : Something error happened\n\n' % (current_time)
        #not signed before , and signed successed
        elif flag == 1:
            log = 'Log time : %s\nMessage : Signed Success\tCurrent point : %s\tExpired date : %s\n\n' % (current_time , input_point , input_expiredate)
        #not signed before , but signed failed
        elif flag == 2:
            log = 'Log time : %s\nMessage : Signed failed\n\n' % (current_time)
        #already signed
        elif flag == 3:
            log = 'Log time : %s\nMessage : Already Signed\tCurrent point : %s\tExpired date : %s\n\n' % (current_time , input_point , input_expiredate)

        if self.Num:
            filename = 'log%d.txt' % (self.Num)
            with open(filename , 'a') as f:
                f.write(log)
        else:
            with open('log.txt' , 'a') as f:
                f.write(log)     

    def check_expire(self , date , reciver):
        current_date = 'Today is : %s-%s-%s' % (datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
        
        date_tmp = datetime.datetime.now() + datetime.timedelta(days=10)
        ten_days_expired = '%s-%s-%s' % (date_tmp.year , date_tmp.month , date_tmp.day)
        
        expire_day_tmp = date.split('-')
        expire_day = '%d-%d-%d' % (int(expire_day_tmp[0]) , int(expire_day_tmp[1]) , int(expire_day_tmp[2]))

        #print expire_day ,  ten_days_expired

        if expire_day == ten_days_expired:
            
            warning = Notifer('id@domain' , 'pwd')
            warning.login()
            warning.sendmail('Point Warning' , current_date + '\n10days points will be expired!!' , reciver)
            warning.close_smtp()
        

        
        

if __name__ == '__main__':
    email = 'id@domain'
    password = 'pwd'

    a = auto_login(email , password)
    if a.login() == 1:
        print 'login failed'
    else:
        expired_day = a.click_button()
        if not expired_day == None:
            a.check_expire(expired_day , 'id@domain')
        a.close_browser()
    


