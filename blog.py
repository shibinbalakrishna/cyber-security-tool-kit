from flask import Flask,render_template,session,jsonify,request,redirect
from flask_session import Session
from flask_cors import CORS
import sqlite3
import requests
from werkzeug.utils import secure_filename
import os
from bs4 import BeautifulSoup as soup



def getNewsData():
  link = "https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en"
  resp=requests.request(method="GET",url=link)
  soup_parser = soup(resp.text, "html.parser")
  ls = soup_parser.find_all("a", class_="DY5T1d")[:10]
  data=[]
  for i in ls:    data.append([i.text[:100]+'...','https://news.google.com'+i.get('href')[1:]])
  return data
def bmData(usrid,msgid):
  conn  = sqlite3.connect('data.db')
  conn.execute("insert into bookmarks (usrid,messageid) values(?,?)",(usrid,int(msgid)))
  conn.commit()
  
def rmData(usrid,msgid):
  conn = sqlite3.connect('data.db')
  conn.execute("delete from bookmarks where messageId={} and usrid='{}'".format(int(msgid),usrid))
  conn.commit()
  
def removeData(val):
  conn  = sqlite3.connect('data.db')
  conn.execute("delete from tweets where messageId={}".format(int(val)))
  conn.execute("delete from comments where messageId={}".format(int(val)))
  conn.execute("delete from retweet where messageId={}".format(int(val)))
  conn.execute("delete from likes where messageId={}".format(int(val)))
  conn.execute("delete from bookmarks where messageId={}".format(int(val)))
  conn.commit()
  
def removeLike(val):
  conn = sqlite3.connect('data.db')
  conn.execute("delete from likes where messageId={} and usrid='{}'".format(int(val),session['name']))
  conn.commit()
  
def removeRetweet(val):
  conn = sqlite3.connect('data.db')
  conn.execute("delete from retweet where messageId={} and usrid='{}'".format(int(val),session['name']))
  conn.commit()
  
def readBookmarkData(usrid):
  conn = sqlite3.connect('data.db')
  ls = []
  usrname,loc = [i for i in conn.execute('select usr,url from user where usrid="{}"'.format(usrid))][0]
  for i in conn.execute("select * from tweets as a inner join bookmarks as b on a.messageid = b.messageid where b.usrid='{}' order by a.messageid".format(usrid)):
    val = list(i)[:len(i)-2]
    val.append(1)
    usrname,loc = [i for i in conn.execute('select usr,url from user where usrid="{}"'.format(i[1]))][0]
    val.append(usrname)
    val.append(loc)
    ls.append(val)
  return ls,loc,usrname

def getCommentsData(msgid):
  conn = sqlite3.connect('data.db')
  query = "select a.messageid,a.comments,a.usrid,b.usr,b.url from comments as a inner join user as b on a.usrid = b.usrid where messageid={} order by a.messageid".format(msgid)
  ls = [list(i) for i in conn.execute(query)][::-1]
  return ls
  
def getProfileData(usrid):
  conn = sqlite3.connect('data.db')
  usr,url = [i for i in conn.execute('select usr,url from user where usrid="{}"'.format(session['name']))][0]
  a,b,c = [i for i in conn.execute('select usr,usrid,url from user where usrid="{}"'.format(usrid))][0]
  ls = []
  ls.append(a)
  ls.append(b)
  ls.append(c)
  ls.append([i for i in conn.execute('select count(*) from tweets where usrid = "{}"'.format(usrid))][0][0])
  query = "select a.msg,a.date,count(*) from tweets as a inner join likes as b on a.messageid=b.messageid where a.usrid='{}' group by b.messageid order by count(*) desc LIMIT 5".format(usrid)
  popular = [i for i in conn.execute(query)]
  if len(popular)==0:
    flag = 0
  else:
    flag = 1
  query = "select a.messageid,a.usrid,c.usr,a.date,c.url,a.msg from tweets as a inner join retweet as b on a.messageid=b.messageid inner join user as c on a.usrid=c.usrid where b.usrid='{}' order by b.messageid desc".format(usrid) 
  retweet = [i for i in conn.execute(query)]
  if len(retweet):
    rflag = 1
  else:
    rflag = 0
  return ls,usr,url,popular,flag,retweet,rflag
  
def readData(frm,range=6):
  max = getMaxMessageId()
  start = max-range+1
  end = max-range+6
  conn  = sqlite3.connect('data.db')
  ls = []
  bmks =[int(i[0]) for i in conn.execute('select messageId from bookmarks where usrid="{}"'.format(session['name']))]
  liked = [i[0] for i in conn.execute('select messageId from likes where usrid="{}"'.format(session['name']))]
  retweet = [i[0] for i in conn.execute('select messageId from retweet where usrid="{}"'.format(session['name']))]
  if frm=='main':
    query = "select * from tweets order by messageId desc".format(start,end)
  else:
    query= "select * from tweets where usrid ='{}'  order by messageId desc".format(session['name'])
  for i in conn.execute(query):
    i=list(i)
    i[3] = "/".join(list(i[3].split('-')))
    if i[0] in bmks:
      i.append(1)
    else:
      i.append(0)
    usrname,loc = [i for i in conn.execute('select usr,url from user where usrid="{}"'.format(i[1]))][0]
    i.append(usrname)
    i.append(loc)
    i.append([_ for _ in conn.execute('select count(*) from likes where messageid={}'.format(i[0]))][0][0])
    if i[0] in liked:
      i.append(1)
    else:
      i.append(0)
    i.append([_ for _ in conn.execute('select count(*) from retweet where messageid={}'.format(i[0]))][0][0])
    if i[0] in retweet:
      i.append(1)
    else:
      i.append(0)
   
    i.append([_ for _ in conn.execute("select count(*) from comments where messageid={}".format(i[0]))][0][0])
    ls.append(i)
  usrname,loc = [i for i in conn.execute('select usr,url from user where usrid="{}"'.format(session['name']))][0]
  return [ls,loc,usrname]
  
def getMaxMessageId():
  conn = sqlite3.connect('data.db')
  val = [i for i in conn.execute("select max(messageid) from tweets")][0][0]
  if val:
    return val
  return 1000000

def insertComment(msgid,msg):
  conn = sqlite3.connect("data.db")
  query="insert into comments(messageid,comments,usrid) values(?,?,?)"
  conn.execute(query,(msgid,msg,session['name']))
  conn.commit()
  query="select usr,url from user where usrid = '{}'".format(session['name'])
  usr,url = [i for i in conn.execute(query)][0]
  return [msgid,msg,session['name'],usr,url,[_ for _ in conn.execute("select count(*) from comments where messageid={}".format(msgid))][0][0]]
def insertLike(val):
  conn = sqlite3.connect("data.db")
  query="insert into likes(messageid,usrid) values(?,?)"
  conn.execute(query,(int(val),session['name']))
  conn.commit()
def insertRetweet(val):
  conn = sqlite3.connect("data.db")
  query="insert into retweet(messageid,usrid) values(?,?)"
  conn.execute(query,(int(val),session['name']))
  conn.commit()
def insertData(val):
  conn  = sqlite3.connect('data.db')
  query="insert into tweets (messageid,usrid,msg,date) values (?,?,?,?)"
  val=(getMaxMessageId()+1,session['name'],val[0],val[1])
  conn.execute(query,val)
  conn.commit()


 
  

