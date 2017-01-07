# -*-coding=utf-8-*-
__author__ = 'Rocky'
#只要把问题的的ID传入即可
#getAll_Answer(id) ，就会返回所有答案。

import urllib2,json,requests,urllib,re
user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
x_req='XMLHttpRequest'
header = {"User-Agent": user_agent,'X-Requested-With':x_req}
def getNext(answerID,offset):
        request_url='https://www.zhihu.com/node/QuestionAnswerListV2'
        #print answerID
        params=json.dumps({"url_token":answerID,"pagesize":"10","offset":offset})
        data={'method':'next','params':params}
        post_data=urllib.urlencode(data)
        # 构造header 伪装一下

        req=urllib2.Request(url=request_url,data=post_data,headers=header)
        resp=urllib2.urlopen(req).read()
        #返回的是str， 转成dict
        resp_dict=json.loads(resp)
        #print resp_dict
        return resp_dict['msg']

def getAnswer(link):
    p='<div class="zm-editable-content clearfix">(.*?)</div>'
    #test_link="https://www.zhihu.com/question/50737023/answer/123268369"
    req=urllib2.Request(url=link,headers=header)
    content=urllib2.urlopen(req).read()
    #print content
    s=re.findall(p,content,re.S)
    if len(s)==0:
        return 0
    return s[0]

def getOffset(answerID):
    request_url='https://www.zhihu.com/question/'+str(answerID)
    #print request_url
    req=urllib2.Request(url=request_url,headers=header)
    content=urllib2.urlopen(req).read()
    #print content
    pattern=re.compile(r'<h3 data-num="\d+" id="zh-question-answer-num">(\d+) 个回答</h3>')

    result=pattern.findall(content)
    if len(result)==0:
        return 0
    #print result
    new_result=result[0]
    offset=(int(new_result)/10)
    return offset

def getAll_Answer(answerID):
    #answerID=50737023
    offset=getOffset(answerID)
    #print offset
    content=[]
    lists=[]
    p='<a href="/question/%s/answer/(\d+)"'  % str(answerID)
    #print p
    #answerID_pattern=re.compile(p,)
    for i in range(offset+1):
        temp=getNext(answerID,i*10)
        #print temp
        print type(temp)
        print len(temp)
        #print temp
        for k in temp:
            #print k
            #如果是图片就忽略，因为图片没有 文字，没有p
            id_list=re.findall(p,k,re.S|re.M)
            if len(id_list) >0:
                lists.append(id_list[0])
        '''
        for k in id_list:
            print k
        #type(temp)
        #content.extend(id_list)
        '''
    print lists
    all_answer=[]
    each_answer='https://www.zhihu.com/question/%s/answer/' % str(answerID)
    for x in lists:
        link=each_answer+x
        result=getAnswer(link)
        #print result
        all_answer.append(result)

    return all_answer

#print id_list


#getAll_Answer(123)
'''
p='<div class="zm-editable-content clearfix">(.*?)</div>'
link="https://www.zhihu.com/question/50737023/answer/123268369"
req=urllib2.Request(url=link,headers=header)
content=urllib2.urlopen(req).read()
#print content
s=re.findall(p,content,re.S|re.M)
print s[0]
'''
'''
print content[0]
author=re.compile(r'<a class="author-link"data-hovercard="p$t$dwill"
target="_blank" href="/people/dwill"
>DWill</a>')
'''

def test_link():
    answerID=28672128
    lnk="https://www.zhihu.com/question/28672128/answer/52384944"
    req=urllib2.Request(url=lnk,headers=header)
    content=urllib2.urlopen(req).read()
    print content
    p='<a href="/question/%s/answer/(\d+)"'  % str(answerID)
    #p='<a href="/question/%s/answer/(\d+)"'  % str(answerID)
    print p
    id_list=re.findall(p,content,re.S|re.M)
    print id_list


#getAll_link()
if __name__=='__main__':
    test_link()