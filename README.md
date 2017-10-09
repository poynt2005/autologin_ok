# autologin_ok

## login_ok.py
> ### The script use "mechanize" library 
> ### Usage : Use the script with crontab to automatically execute the script
```
1. chmod +x login_ok.py

2. crontab -e

3. in crontab insert : "12 * * * * cd ~/your directory/ && /usr/bin/python2.7 ~/your directory/login_ok.py"
```
>> * method *"login()"* will login to the website , return 1 if login failed
>> * method *"click_button()"* emulate clicking the "Sign" button in user modules page
>>> *if it hasn't signed , it will sign , and then call "get_point(input_text , flag)" method to calculate points , sed id to 1*
>>> *if it hasn't signed , and signed failed , set id to 2*
>>> *if it has already signed , call "get_point(input_text , flag)" method to calculate points , set id to 3*
>>> *other else set id to 0*
>> * method "get_point(input_text , flag)" use regex to find points and expire day , and return expire day
>> * method "write_log(input_point , input_expiredate, flag)" generate a log file , log message is determined by flag(id number) and it will record current points and expire day to log file*
>> * method "check_expire(date , reciver)" send warning email to "reciver" if it is only 10 days before the points expired

## mailnotifer_pchome.py
> ### The script emails notifer mail to reciver using pchome smtp server and python smtplib



