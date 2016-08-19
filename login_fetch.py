# -*-coding=utf-8-*-
__author__ = 'Rocky'
import requests
import cookielib
import re
import json
import time
import StringIO
import Image
import os
from getContent import GetContent
agent='Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers={'Host':'www.zhihu.com',
         'Referer':'https://www.zhihu.com',
         'User-Agent':agent}

#全局变量
session=requests.session()

session.cookies=cookielib.LWPCookieJar(filename="cookies")

try:
    session.cookies.load(ignore_discard=True)
except:
    print "Cookie can't load"

def isLogin():
    url='https://www.zhihu.com/settings/profile'
    login_code=session.get(url,headers=headers,allow_redirects=False).status_code
    print login_code
    if login_code == 200:
        return True
    else:
        return False

def get_xsrf():
    url='http://www.zhihu.com'
    r=session.get(url,headers=headers,allow_redirects=False)
    txt=r.text
    result=re.findall(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"/>',txt)[0]
    return result

def getCaptcha():
    #r=1471341285051
    r=(time.time()*1000)
    url='http://www.zhihu.com/captcha.gif?r='+str(r)+'&type=login'

    image=session.get(url,headers=headers)
    f=open("photo.jpg",'wb')
    f.write(image.content)
    f.close()


def Login():
    xsrf=get_xsrf()
    print xsrf
    print len(xsrf)
    login_url='http://www.zhihu.com/login/email'
    data={
    '_xsrf':xsrf,
    'password':'*',
    'remember_me':'true',
    'email':'*'
    }
    try:
        content=session.post(login_url,data=data,headers=headers)
        login_code=content.text
        print content.status_code
        #this line important ! if no status, if will fail and execute the except part
        #print content.status

        if content.status_code != requests.codes.ok:
            print "Need to verification code !"
            getCaptcha()
            #print "Please input the code of the captcha"
            code=raw_input("Please input the code of the captcha")
            data['captcha']=code
            content=session.post(login_url,data=data,headers=headers)
            print content.status_code

            if content.status_code==requests.codes.ok:
                print "Login successful"
                session.cookies.save()




            #print login_code
        else:
            session.cookies.save()
    except:
        print "Error in login"
        return False

def focus_question():
    focus_id=[]
    url='https://www.zhihu.com/question/following'
    content=session.get(url,headers=headers)
    print content
    p=re.compile(r'<a class="question_link" href="/question/(\d+)" target="_blank" data-id')
    id_list=p.findall(content.text)
    pattern=re.compile(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"/>')
    result=re.findall(pattern,content.text)[0]
    print result
    for i in id_list:
        print i
        focus_id.append(i)

    url_next='https://www.zhihu.com/node/ProfileFollowedQuestionsV2'
    page=20
    offset=20
    end_page=500
    xsrf=re.findall(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"',content.text)[0]
    while offset < end_page:
        #para='{"offset":20}'
        #print para
        print "page: %d" %offset
        params={"offset":offset}
        params_json=json.dumps(params)

        data={
        'method':'next',
        'params':params_json,
        '_xsrf':xsrf
        }
        #print data
        offset=offset+page
        headers_l={
        'Host':'www.zhihu.com',
        'Referer':'https://www.zhihu.com/question/following',
        'User-Agent':agent,
        'Origin':'https://www.zhihu.com',
        'X-Requested-With':'XMLHttpRequest'
        }
        try:
            s=session.post(url_next,data=data,headers=headers_l)
            #print s.status_code
            #print s.text
            msgs=json.loads(s.text)
            msg=msgs['msg']
            for i in msg:
                id_sub=re.findall(p,i)
                #print i
                for j in id_sub:
                    print j
                    id_list.append(j)
                #print i
                #list_left=p.findall(j)

            #for j in list_left:
            #   print j

        except:
            print "Getting Error "


    return id_list

def main():

    if isLogin():
        print "Has login"
    else:
        print "Need to login"
        Login()
    list_id=focus_question()
    for i in list_id:
        print i
        obj=GetContent(i)

    #getCaptcha()
if __name__=='__main__':
    sub_folder=os.path.join(os.getcwd(),"content")
    #专门用于存放下载的电子书的目录

    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)

    os.chdir(sub_folder)

    main()