import smtplib
import datetime

class Notifer_pchome(object):
    def __init__(self , id_number , password):
        self.id_number = id_number
        self.password = password
        self.mail = smtplib.SMTP()
        #self.mail.set_debuglevel(1)
        self.mail.connect('smtp.pchome.com.tw' , 25)

    def login(self):
        try:
            self.mail.ehlo()
            self.mail.starttls()
            self.mail.ehlo()
            self.mail.esmtp_features['AUTH'] = 'PLAIN LOGIN'
            self.mail.login(self.id_number , self.password)
            
        except :
            self.write_log('login failed')
           # print 'login failed'
        else:
            self.write_log('login success')
           # print 'login success'

    def sendmail(self , subject , content , reciver):
        message = 'From: %s\nTo: %s\nSubject: %s\n%s' % (self.id_number , reciver , subject , content)    
        try:
            self.mail.sendmail(self.id_number , reciver , message)
        except:
            self.write_log('sended failed')
           # print 'sended failed'
        else:
            self.write_log('sended success')
           # print 'sended success' 
                  
    def close_smtp(self):
        self.mail.quit()
    
    def write_log(self , message):
        current_time = str(datetime.datetime.now())

        log_message = 'Current time : %s\nTry to send mail : %s\n\n' % (current_time , message)
        with open('log.txt' , 'a') as f:
            f.write(log_message)

def main():
    a = Notifer_pchome('id@domain' , 'pwd')
    a.login()
    a.sendmail('Warning' , 'Test Warning' , 'id@domain')
    a.close_smtp()

if __name__ == '__main__':
    main()
