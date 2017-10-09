from login_ok import auto_login
import threading


def job(num):
    email = 'id%d@domain' % (num)
    password = 'password%d' % (num)

    a = auto_login(email , password , num)
    if a.login() == 1:
        print 'login failed'
    else:
        expired_day = a.click_button()
        if not expired_day == None:
            a.check_expire(expired_day , 'id@domain')
        a.close_browser()


def main():
    for i in range(0,3,1):
        t = threading.Thread(target = job , args = (i,))
        t.start()

if __name__ == '__main__':
    main()
