from autoLogin import autoLogin
import json
import datetime

def writeToLog(currentId , signMessage ,error = False):
    with open('log.txt' , 'a') as f:
        if not error:
            f.write('Logged ID : %s , currentTime : %s , %s\n' % (currentId , datetime.datetime.now() , signMessage))
        else:
            f.write('Logged ID : %s , currentTime : %s , Signed Failed ,maybe connection error or id incorrent\n' % (currentId , datetime.datetime.now()))
    return
def writeToJson(messageArr):
    with open('currentState.json' , 'w') as f:
        j = json.dumps(messageArr , ensure_ascii=False)
        f.write(j)
    return

def main():
    res = []
    email = ''
    password = ''

        try:
            a = autoLogin(email=email , pwd=password)
            a.login()
            a.sign()
            mes = a.getMessage()
            
            writeToLog(email , mes['state'])
            res.append(mes)
        except:
            writeToLog(email ,'' ,  True)
    if res:
        writeToJson(res)


if __name__ == '__main__':
    main()
