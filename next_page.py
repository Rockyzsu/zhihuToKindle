# -*-coding=utf-8-*-
__author__ = 'Rocky'
import urllib2,json,requests,urllib,re
user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
x_req='XMLHttpRequest'
header = {"User-Agent": user_agent,'X-Requested-With':x_req}
def getNext(answerID,offset):
        request_url='https://www.zhihu.com/node/QuestionAnswerListV2'
        print answerID
        params=json.dumps({"url_token":answerID,"pagesize":"10","offset":offset})
        data={'method':'next','params':params}
        post_data=urllib.urlencode(data)
        # 构造header 伪装一下

        req=urllib2.Request(url=request_url,data=post_data,headers=header)
        resp=urllib2.urlopen(req).read()
        #返回的是str， 转成dict
        resp_dict=json.loads(resp)
        return resp_dict['msg']

def getOffset(answerID):
    request_url='https://www.zhihu.com/question/'+str(answerID)
    req=urllib2.Request(url=request_url,headers=header)
    content=urllib2.urlopen(req).read()
    #print content
    pattern=re.compile(r'<h3 data-num="\d+" id="zh-question-answer-num">(\d+) 个回答</h3>')
    result=pattern.findall(content)[0]
    print result
    offset=(int(result)/10)
    return offset

answerID=50737023
offset=getOffset(answerID)
print offset
content=[]
for i in range(offset+1):
    temp=getNext(answerID,i*10)
    content.extend(temp)

print len(content)

print content[0]
author=re.compile(r'<a class="author-link"data-hovercard="p$t$dwill"
target="_blank" href="/people/dwill"
>DWill</a>')