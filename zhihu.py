import smtplib
import time,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from email.MIMEBase import MIMEBase
from email import Encoders
import urllib2,urllib,time,datetime,codecs,sys,re,sys
from mail_template import MailAtt
reload(sys)
sys.setdefaultencoding('utf-8')

def save2file(filename,content):
	'''
	sub_folder=os.path.join(os.getcwd(),"content")
	if not os.path.exists(sub_folder):
		os.mkdir(sub_folder)
	filename_path=os.path.join(sub_folder,filename+".txt")
	
	f=open(filename_path,'a')
	'''
	filename=filename+".txt"
	f=open(filename,'a')
	f.write(content)
	f.close()

def save2file_ch(filename,content):
	filename=filename+".txt"
	f=codecs.open(filename,'a')
	f.write(content)
	f.close()

def send_attachment(filename,toName,fromName,username,password):
	filename_txt=filename+".txt"
	print filename_txt.decode('utf-8')
	filecontent=open(filename_txt.decode('utf-8'),'r').read()
	att=MIMEText(filecontent,'base64','utf-8')
	att['Content-Type']='application/octet-stream;name="Hello.txt'
	att['Content-Disposition'] ='attachment; filename="Hello.txt"'
	att['Content-Transfer-Encoding']='base64'
	print att["Content-Disposition"]
	
	msg=MIMEMultipart()
	msg.attach(att)
	msg['To']=toName
	msg['From']=username+"<"+fromName+">"
	msg['Subject']=filename
	print "Subject"
	print msg['Subject']
	try:
		server=smtplib.SMTP()
		server.connect('smtp.qq.com')
		server.login(username,password)
		server.sendmail(msg['From'],toName,msg.as_string())
		server.quit()
		print "Send successfully"
	except Exception,e:
		print "Error"
		print str(e)	

def send_attachment_kd(filename,toName,fromName,username,password):
    msg = MIMEMultipart()
    msg['Subject'] = 'convert'
    msg['From'] = "yourname"+"<"+fromName+">"
    msg['To'] = toName
    part = MIMEBase('application', "octet-stream")
    #fpath=os.path.join(KINDLE_DIR,filename)
    filename_txt=filename+".txt"
    #print filename_txt.decode('utf-8'
    filecontent=open(filename_txt.decode('utf-8'),'r').read()
    part.set_payload(filecontent)
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Zhi Hu.txt"')
    msg.attach(part)
    try:
        server=smtplib.SMTP()
        server.connect('smtp.qq.com')
        server.login(username,password)
        server.sendmail(msg['From'],toName,msg.as_string())
        server.quit()
        print "Send successfully"
    except Exception,e:
        print "Error"
        print str(e)


def getAnswer(answerID):
	host="http://www.zhihu.com"
	url=host+answerID
	print url
	user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
	header={"User-Agent":user_agent}
	req=urllib2.Request(url,headers=header)
	resp=urllib2.urlopen(req)
	
	#save2file("temp.txt",resp.read())
	#title=
	
	#resp=open("temp.txt",'r')
	bs=BeautifulSoup(resp,"html.parser")
	title=bs.title
	#print type(title)
	#print type(title.string)
	filename_old=title.string.strip()
	print filename_old
	filename = re.sub('[\/:*?"<>|]','-',filename_old)
	save2file(filename,title.string)
	title_content=title.string
	
	answer=[]
	# use sub ?
	detail=bs.find("div",class_="zm-editable-content")
	user_ids=bs.find_all("a",class_="author-link")
	#print detail.strings
	#print type(detail) 
	# user_ids[0].string
	
	save2file(filename,"\n\n\n\n--------------------Detail----------------------\n\n")
	#save detail content
	
	for i in detail.strings:
		#print i
		#clean_tag=i.strings
		#print i.strings
		#print i
		save2file(filename,unicode(i))
	#details=detail.div.contents
	'''
	k=0
	for i in details:
		print k
		print unicode(i)
		k+=1
	'''
	#print details
	'''
	print detail.children
	for i in detail.children:
		print i.string
	'''
	'''
	for i in detail:
		if type(i):
			print i.string
	'''
		#print detail.string
	#save2file(answerID,unicode(title.string))
	#detail=bs.
	#
	#save2file("temp.txt","HEEELO")
	
	
	#save all answer link:
	#save2file(filename,"\n-------------------------answer-------------------------\n")
	
	
	answer=bs.find_all("div",class_="zm-editable-content clearfix")
	k=0
	index=0
	for each_answer in answer:
		#print each_answer
		#print user_ids[index].string
		
		save2file(filename,"\n\n-------------------------answer %s via  -------------------------\n\n" %k)
		
		
		for a in each_answer.strings:
			#clean_a_tag=a.strings
			#print a
			save2file(filename,unicode(a))
		k+=1
		index=index+1
	
	#filename="source1.txt"
	#toName="yourname@kindle.cn"
	#oName="yourname@kindle.cn"
	#fromName="yourname@126.com"
	#username="yourname"
	#txt_filename=filename
	#send_attachment(filename,toName,fromName,username,password)
	
	smtp_server='smtp.126.com'
	from_mail='your@126.com'
	password='yourpassword'
	#to_mail='yourname@qq.cn'
	to_mail='yourname@kindle.cn'
	send_kindle=MailAtt(smtp_server,from_mail,password,to_mail)
	#sub_folder=os.path.join(os.getcwd(),"content")
	#filename_path=os.path.join(sub_folder,filename+".txt")
	print filename
	#send_kindle.send_txt(filename)

	
def check_mail():
	filename="test2"
	smtp_server='smtp.126.com'
	from_mail='yourname@126.com'
	password='yourpassword'
	to_mail='yourkindlemail@kindle.cn'
	send_kindle=MailAtt(smtp_server,from_mail,password,to_mail)
	#sub_folder=os.path.join(os.getcwd(),"content")
	#filename_path=os.path.join(sub_folder,filename+".txt")
	print filename
	send_kindle.send_txt(filename)
	
def read_content(filename):
	#why i can't read chinese here ???????
	print "Hello"	
	try:
		print "working now"
		f=codecs.open(filename,'r','utf-8')
		#content=f.read()
		print "loading"
		j=0
		for i in f.readline():
			print j
			print i
			j+=1
	#print content
		f.close()
	except Exception:
		print "Error"
		f.close()
	finally:
		f.close()

def getLink(original):
	link=[]
	user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
	header={"User-Agent":user_agent}
	req=urllib2.Request(original,headers=header)
	resp=urllib2.urlopen(req)
	bs=BeautifulSoup(resp.read(),"html.parser")
	#print type(bs)
	l=bs.find_all("a",class_="question_link")
	for i in l:
		reg_l=i['href']
		answer_lnk=reg_l.split('/')[0:3]
		new_answer_lnk='/'.join(answer_lnk)
		#print answer_lnk
		link.append(new_answer_lnk)
	return link
		
if __name__=="__main__":
	#getAnswer("/question/37334863")
	#read_content("ten.txt") not working
	#link=getLink("http://www.zhihu.com/explore/recommendations")
	sub_folder=os.path.join(os.getcwd(),"content")
	if not os.path.exists(sub_folder):
		os.mkdir(sub_folder)
	#filename_path=os.path.join(sub_folder,filename+".txt")
	os.chdir(sub_folder)
	id=sys.argv[1]
	id_link="/question/"+id
	getAnswer(id_link)
	#check_mail()
	#time.sleep(10)
	#print link
	'''
	for i in link:
		getAnswer(i)
		time.sleep(10)
		
		print "Done inside"
	'''
	print "Done"
	
	
