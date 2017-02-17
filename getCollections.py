# -*-coding=utf-8-*-
__author__ = 'Rocky'
import requests
import cookielib
import re
import json
import time
from bs4 import BeautifulSoup
import os
from lxml import etree
import codecs

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
def save2file(filename, content):
    # 保存为电子书文件
    filename = filename + ".txt"
    f = codecs.open(filename, 'a',encoding='utf-8')
    f.write(content)
    f.close()

def getAnswer(url):
    #这个功能已经实现
    html=session.get(url,headers=headers,allow_redirects=False)
    s=html.text

    tree=etree.HTML(s)
    title=tree.xpath('//title/text()')[0]

    filename_old = title.strip()
    filename = re.sub('[\/:*?"<>|]', '-', filename_old)
    # 用来保存内容的文件名，因为文件名不能有一些特殊符号，所以使用正则表达式过滤掉
    print filename
    save2file(filename, title)

    save2file(filename, "\n\n--------------------Link %s ----------------------\n"  %url)
    save2file(filename, "\n\n--------------------Detail----------------------\n\n")
    # 获取问题的补充内容
    content=tree.xpath('//div[@class="zm-editable-content clearfix"]/text()')
    for i in content:
        #print i
        save2file(filename,i)


def getCollections():
    #实现，获取所有的collection 的link
    links=[]
    url='https://www.zhihu.com/collections/mine'
    Login()

    if isLogin():
        content=session.get(url,headers=headers,allow_redirects=False)
        s= content.text

        p=re.compile(r'<h2 class=\"zm-item-title\">\s+<a href=\"(.*?)\" >')
        result=p.findall(s,re.S)
        if result is not None:
            return result
        else:
            return None

def getEachQuestion(url):
    s=session.get(url,headers=headers,allow_redirects=False)
    tree=etree.HTML(s.text)
    result=tree.xpath('//link[@itemprop="url"]/@href')
    return result


if __name__=='__main__':

    collection_link=getCollections()
    '''
    collection=['https://www.zhihu.com'+i for i in collection_link]
    print collection
    '''
    for i in collection_link:
        link="https://www.zhihu.com"+i
        
    #url='https://www.zhihu.com/collection/40627095'
    #getEachQuestion(url)
    #getAnswer('https://www.zhihu.com/question/30348020/answer/144386645')