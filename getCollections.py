# -*-coding=utf-8-*-
__author__ = 'Rocky'
import requests
import cookielib
import re
import json
import time
import os
session = requests.session()

session.cookies = cookielib.LWPCookieJar(filename="cookies")
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {'Host': 'www.zhihu.com',
           'Referer': 'https://www.zhihu.com',
           'User-Agent': agent}
try:
    session.cookies.load(ignore_discard=True)
except:
    print "Cookie can't load"

def getUserData(configFile):
    f = open(configFile, 'r')

    #for i in f.readlines():
    data=f.readlines()
    username=data[0].strip()
    pwd=data[1].strip()
    return username,pwd

def getCaptcha():
    #r=1471341285051
    r = (time.time() * 1000)
    url = 'http://www.zhihu.com/captcha.gif?r=' + str(r) + '&type=login'

    image = session.get(url, headers=headers)
    f = open("photo.jpg", 'wb')
    f.write(image.content)
    f.close()
def get_xsrf():
    url = 'https://www.zhihu.com'
    r = session.get(url, headers=headers, allow_redirects=False)
    txt = r.text
    #print txt
    result = re.findall(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"/>', txt)[0]
    return result

def Login():
    username,pwd=getUserData("data.cfg")
    xsrf = get_xsrf()
    print xsrf
    print len(xsrf)
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        '_xsrf': xsrf,
        'password': pwd,
        'remember_me': 'true',
        'email': username
    }
    try:
        content = session.post(login_url, data=data, headers=headers)
        login_code = content.text
        d = json.loads(login_code)
        #print d['msg']
        #print content.status_code
        #this line important ! if no status, if will fail and execute the except part
        #print content.status

        if content.status_code != requests.codes.ok:
            print "Need to verification code !"
            getCaptcha()
            #print "Please input the code of the captcha"
            code = raw_input("Please input the code of the captcha")
            data['captcha'] = code
            content = session.post(login_url, data=data, headers=headers)
            print content.status_code

            if content.status_code == requests.codes.ok:
                print "Login successful"
                session.cookies.save()
                #print login_code
        else:
            session.cookies.save()
            return True
    except:
        print "Error in login"
        return False

def isLogin():
    url = 'https://www.zhihu.com/settings/profile'
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    print login_code
    if login_code == 200:
        return True
    else:
        return False

def getCollections():
    links=[]
    url='https://www.zhihu.com/collections/mine'
    Login()

    if isLogin():
        content=session.get(url,headers=headers,allow_redirects=False)
        s= content.text
        print s

        p=re.compile(r'<h2 class=\"zm-item-title\">\s+<a href=\"(.*?)\" >')
        result=p.findall(s,re.S)
        print result
        if result is not None:
            for i in result:
                #print i
                links.append(i)
        print links
    return links

def gerEachQuestion(url):
    url="https://www.zhihu.com"+url
    p=r'<h2 class="zm-item-title"><a target="_blank" href="/question/(\d+)">'
    content=session.get(url,headers=headers,allow_redirects=False)
    s= content.text
getCollections()
