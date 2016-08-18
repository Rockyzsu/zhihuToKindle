# -*-coding=utf-8-*-
__author__ = 'Rocky'
import requests
import cookielib
import re
import json
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

def Login():
    xsrf=get_xsrf()
    print xsrf
    print len(xsrf)
    login_url='http://www.zhihu.com/login/email'
    data={
    '_xsrf':xsrf,
    'password':'xxxxxx',
    'captcha_type':'cn',
    'remember_me':'true',
    'email':'xxxxxx@126.com'
    }

    content=session.post(login_url,data=data,headers=headers)
    print content.status_code
    print content.text
    session.cookies.save()

def focus_question():
    focus_id=[]
    url='https://www.zhihu.com/question/following'
    content=session.get(url,headers=headers)
    print content
    p=re.compile(r'<a class="question_link" href="/question/(\d+)" target="_blank" data-id')
    id_list=p.findall(content.text)
    result=re.findall(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"/>',content.text)[0]
    print result
    for i in id_list:
        print i
        focus_id.append(i)

    url_next='https://www.zhihu.com/node/ProfileFollowedQuestionsV2'
    page=20
    offset=20
    end_page=10000
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
        print data
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
            print s.text
            msgs=s.text
            msg=msgs['msg']
            for i in msg:
                print i
            #list_left=p.findall(s.text)
            #for j in list_left:
            #   print j
        except:
            print "Getting Error "

def main():
    if isLogin():
        print "Has login"
    else:
        Login()
    focus_question()

if __name__=='__main__':
    main()