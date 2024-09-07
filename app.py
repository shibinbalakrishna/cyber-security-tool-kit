#importing required libraries

from flask import Flask, request, render_template,Response,session,jsonify,request,redirect
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import requests
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore')
from feature import generate_data_set
# Gradient Boosting Classifier Model
from sklearn.ensemble import GradientBoostingClassifier
from script import *
import dpkt,pygeoip
from feature import *
from password import *
from urllib.parse import urlparse



from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_mail import Mail, Message
import random
import hashlib
import os
import io
import string
from werkzeug.utils import secure_filename
import ssl
import socket
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import time
from tqdm import tqdm
from virus_total_apis import PublicApi as vtPubAPI



from flask_session import Session
from flask_cors import CORS
import sqlite3
import requests
from werkzeug.utils import secure_filename
import os
from bs4 import BeautifulSoup as soup
from blog import *
from mainblog import *
from iptracker import *
from username import *
from websitevuln import *
from basic_vuln import *
from rep import *
from urlclean import *


import hashlib
import io
from PIL import Image
import cv2

def sum(a,b):
  return a+b

ALLOWED_EXTENSIONS = ['jpg','png','jpeg']
UPLOAD_FOLDER = 'static/UserPics'


vt = vtPubAPI("5f2174dcd5bbd7be427f4d400e500dba31afb2527aa53e25bc50cdcad1757e40")


data = pd.read_csv("phishing.csv")
#droping index column
data = data.drop(['Index'],axis = 1)
# Splitting the dataset into dependant and independant fetature

X = data.drop(["class"],axis =1)
y = data["class"]


# instantiate the model
gbc = GradientBoostingClassifier(max_depth=4,learning_rate=0.7)

# fit the model 
gbc.fit(X,y)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)
CORS(app)

vt = vtPubAPI("5f2174dcd5bbd7be427f4d400e500dba31afb2527aa53e25bc50cdcad1757e40")

blacklist = ['example.com', 'google.com', 'yahoo.com']
data_file_path = 'data.data'



@app.route("/")
def main1():
    tweets = get_tweets()
    blog_posts = get_blog_posts()
    return render_template("main1.html",tweets=tweets, blog_posts=blog_posts)



@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
   val,loc,usrname = readData(frm='main')
   return render_template('dashboard.html',data = val,loc=loc,usrname=usrname,usrid=session['name'])

@app.route('/phishing')
def phishing():
    val,loc,usrname = readData(frm='main')
    return render_template('phishing.html', xx= -1,loc=loc)
@app.route("/dashboard2")
def dashboard2():
   return render_template("dashboard2.html")
@app.route("/phishing2")
def phishing2():
   return render_template('phishing2.html', xx=-1)
@app.route("/phishing3")
def phishing3():
   val,loc,usrname = readData(frm='main')
   return render_template('phishing3.html', xx=-1,loc=loc)


@app.route('/disclaimer')
def disclaimer():
    val,loc,usrname = readData(frm='main')
    return render_template('disclaimer.html',loc=loc)

@app.route('/disclaimer2')
def disclaimer2():
    val,loc,usrname = readData(frm='main')
    return render_template('disclaimer2.html',loc=loc)



# @app.route('/phishing')
# def dashboard():
#    return render_template('phishing.html', xx= -1)







@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        msg = ""
        url = request.form["url"]
        msg = scan_url(url)
        x = np.array(generate_data_set(url)).reshape(1,30) 
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('phishing.html',xx =round(y_pro_non_phishing,2),url=url,result=msg )
        # else:
        #     pred = "It is {0:.2f} % unsafe to go ".format(y_pro_non_phishing*100)
        #     return render_template('index.html',x =y_pro_non_phishing,url=url )
    return render_template("phishing.html", xx =-1)

@app.route("/predict2", methods=["GET", "POST"])
def predict2():
    if request.method == "POST":
        msg = ""
        url = request.form["url"]
        msg = scan_url(url)
        x = np.array(generate_data_set(url)).reshape(1,30) 
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('phishing2.html',xx =round(y_pro_non_phishing,2),url=url,result=msg )
        # else:
        #     pred = "It is {0:.2f} % unsafe to go ".format(y_pro_non_phishing*100)
        #     return render_template('index.html',x =y_pro_non_phishing,url=url )
    return render_template("dashboard2.html", xx =-1)

@app.route("/predict3", methods=["GET", "POST"])
def predict3():
    if request.method == "POST":
        msg = ""
        url = request.form["url"]
        msg = scan_url(url)
        x = np.array(generate_data_set(url)).reshape(1,30) 
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('phishing3.html',xx =round(y_pro_non_phishing,2),url=url,result=msg )
        # else:
        #     pred = "It is {0:.2f} % unsafe to go ".format(y_pro_non_phishing*100)
        #     return render_template('index.html',x =y_pro_non_phishing,url=url )
    return render_template("phishing3.html", xx =-1)
@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Perform web scraping here using BeautifulSoup
    
    # Example: Extracting all the links from the page
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    
    return render_template('index2.html', links=links)

@app.route('/check_url', methods=['POST'])
def check_url():
    url = request.form['url']
    
    # Check if the URL is blacklisted
    # if url in blacklist:
    #     result = 'The URL is not blacklisted.'
    # else:
    #     result = 'The URL is  blacklisted.'

    # Check if the URL is present in the .data file
    if check_in_data_file(url):
        result = ' The URL is blacklisted.'
    else:
        result = ' The URL is  not blacklisted.'

    return render_template('blacklist.html', result=result)

def check_in_data_file(url):
    with open('two-level-tlds.data', 'r') as file:
        for line in file:
            if url in line:
                return True
    return False

@app.route('/pcapkml', methods=['GET', 'POST'])
def upload_file():
    val,loc,usrname = readData(frm='main')

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.pcap'):
            val,loc,usrname = readData(frm='main')

            pcap = dpkt.pcap.Reader(file)
            kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
                        '<Style id="transBluePoly">' \
                        '<LineStyle>' \
                        '<width>1.5</width>' \
                        '<color>501400E6</color>' \
                        '</LineStyle>' \
                        '</Style>'
            kmlfooter = '</Document>\n</kml>\n'
            kmldoc = kmlheader + plotIPs(pcap) + kmlfooter

            # Save KML result to a file
            with open('pcapkml.kml', 'w', encoding='utf-8') as kml_file:
                kml_file.write(kmldoc)

            return render_template('pcapkml.html', kmldoc='pcapkml.kml',loc=loc)

    return render_template('pcapkml.html',loc=loc)

@app.route('/pcapkml2', methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.pcap'):
            pcap = dpkt.pcap.Reader(file)
            kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
                        '<Style id="transBluePoly">' \
                        '<LineStyle>' \
                        '<width>1.5</width>' \
                        '<color>501400E6</color>' \
                        '</LineStyle>' \
                        '</Style>'
            kmlfooter = '</Document>\n</kml>\n'
            kmldoc = kmlheader + plotIPs(pcap) + kmlfooter

            # Save KML result to a file
            with open('pcapkml.kml', 'w', encoding='utf-8') as kml_file:
                kml_file.write(kmldoc)

            return render_template('pcapkml2.html', kmldoc='pcapkml.kml')

    return render_template('pcapkml2.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return Response(open(filename, 'rb').read(),
                    mimetype="application/vnd.google-earth.kml+xml",
                    headers={"Content-Disposition": "attachment;filename=" + filename})




@app.route('/password_security', methods=['POST', 'GET'])
def password_strength():
        val,loc,usrname = readData(frm='main')

        if request.method == 'POST':
            password = request.form.get('password')
            result = check_password_strength(password)
            count = pwned_api_check(password)
            if count:
               result1 = f'\"{ password }\"  is found  {count}  times. You should change it'
               return render_template('password-security.html', result=result,result1=result1,loc=loc,count=count,checked=True)
            else:
               result1= f"\"{ password }\" is not  found. You're good to go"
               return render_template('password-security.html', result=result,result1=result1,loc=loc,checked=True)
        return render_template('password-security.html',loc=loc)


@app.route('/password_security2', methods=['POST', 'GET'])
def password_strength2():

        if request.method == 'POST':
            password = request.form.get('password')
            result = check_password_strength(password)
            count = pwned_api_check(password)
            if count:
               result1 = f'\"{ password }\"  is found  {count}  times. You should change it'
               return render_template('password-security2.html', result=result,result1=result1, count=count,checked=True)
            else:
               result1= f"\"{ password }\" is not  found. You're good to go"
               return render_template('password-security2.html', result=result,result1=result1, checked=True)
        return render_template('password-security2.html')

#dir finder
@app.route("/dir_scan", methods=["GET", "POST"])
def dir_scan():
    val, loc, usrname = readData(frm='main')
    if request.method == "POST":
        url = request.form.get("url")

        # Check if the URL has either http:// or https:// prefix
        parsed_url = urlparse(url)
        if not (parsed_url.scheme == "http" or parsed_url.scheme == "https"):
            # If no scheme found, assume http:// as default
            url = "http://" + url

        with open("list.txt", "r") as wordlist_file:
            discovered_dirs = []
            for line in wordlist_file:
                word = line.strip()
                test_url = url + "/" + word
                response = request_url(test_url)
                if response:
                    discovered_dirs.append(test_url)

        return render_template("dir_scan.html", discovered_dirs=discovered_dirs,loc=loc)

    return render_template("dir_scan.html",loc=loc)

def request_url(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass
    

@app.route("/dir_scan2", methods=["GET", "POST"])
def dir_scan2():
    val, loc, usrname = readData(frm='main')
    if request.method == "POST":
        url = request.form.get("url")

        # Check if the URL has either http:// or https:// prefix
        parsed_url = urlparse(url)
        if not (parsed_url.scheme == "http" or parsed_url.scheme == "https"):
            # If no scheme found, assume http:// as default
            url = "http://" + url

        with open("list.txt", "r") as wordlist_file:
            discovered_dirs = []
            for line in wordlist_file:
                word = line.strip()
                test_url = url + "/" + word
                response = request_url(test_url)
                if response:
                    discovered_dirs.append(test_url)

        return render_template("dir_scan2.html", discovered_dirs=discovered_dirs,loc=loc)

    return render_template("dir_scan2.html",loc=loc)

def request_url(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

@app.route("/helppcap",)
def helppcap():
    return render_template("helppcap.html")

@app.route("/helppcap2",)
def helppcap2():
    return render_template("helppcap2.html")






# blog---------------------------------------------------------





@app.route('/home/<value>')
def home(value):
  if not session.get("name") or session['name']!=value:
    session['name'] = None
    return redirect('/')
  val,loc,usrname = readData(frm='main')
  return render_template('index.html',data = val,news=getNewsData(),loc=loc,usrname=usrname,usrid=session['name'])
  
@app.route('/messages/<value>')
def messages(value):
  if not session.get("name") or session['name']!=value:
    session['name'] = None
    return redirect('/')
  val,loc,usrname = readData(frm='msg')
  return render_template('messages.html',data =val,loc=loc,news = getNewsData(),usrname=usrname,usrid=session['name'])
  
@app.route('/bookmarks/<value>')
def bookmarks(value):
  if not session.get("name") or session['name']!=value:
    session['name'] = None
    return redirect('/')
  val,loc,usrname =readBookmarkData(session.get("name"))
  return render_template('bookmarks.html',data = val,news = getNewsData(),usrid=session['name'],loc = loc,usrname=usrname)  
  
@app.route('/profile/<value>')
def profile(value):
  if not session.get("name"):
    session['name'] = None
    return redirect('/')
  val,usr,url,popular,flag,retweet,rflag = getProfileData(value)
  return render_template('profile.html',data = val ,news = getNewsData(),usrid=session["name"],loc=url,usrname=usr,popular=popular,flag=flag,retweet=retweet,rflag=rflag)

@app.route('/logout')
def logout():
  print(session['name'])
  session['name'] = None
  return redirect('/')
@app.route('/home')
def routehome():
  return redirect('/home/'+session['name'])
@app.route('/getComments/<value>',methods=['POST'])
def getComments(value):
  return jsonify({'data':getCommentsData(int(value))})
@app.route('/addComments/<value>',methods=['POST'])
def addComments(value):
  msgid,msg= value.split('-_-')
  return jsonify({'data':insertComment(msgid,msg)})
@app.route('/addRetweet/<value>',methods=['POST'])
def addRetweet(value):
  insertRetweet(value)
  return "True"
@app.route('/deleteRetweet/<value>',methods=['POST'])
def deleteRetweet(value):
  removeRetweet(value)
  return "True"
@app.route('/addLike/<value>',methods=['POST'])
def addLike(value):
  insertLike(value)
  return "True"
@app.route('/deleteLike/<value>',methods=['POST'])
def deleteLike(value):
  removeLike(value)
  return "True"
@app.route('/addData/<value>',methods=['POST'])
def addData(value):
  insertData(value.split("-_-"))
  return "True"
@app.route('/deleteData/<value>',methods=['POST'])
def deleteData(value):
  removeData(value)
  return "True"
@app.route('/bookmarkData/<val>',methods=['POST'])
def bookmarkData(val):
  usrid,msgid = val.split('-')
  bmData(session['name'],msgid)
  return "True"
@app.route('/removebookmark/<val>',methods=['POST'])
def deletemarkData(val):
  usrid,msgid = val.split('-')
  rmData(session['name'],msgid)
  return "True"
  
@app.route('/loaddata/<range>',methods=['POST'])
def loaddata(range):
  range,frm = range.split('-_-')
  data = readData(frm,int(range))[0]
  return jsonify({'data':data,'msgid':getMaxMessageId()})



@app.route('/login')
def login():
  print("Hello")
  return render_template('login.html')

# Login
@app.route('/validateUser/<value>',methods=['POST'])
def validateUser(value):
  usrid,pwd = value.split('-_-')
  conn = sqlite3.connect('data.db')
  if request.method == 'POST':
    if [i for i in conn.execute("select count(*) from user where usrid = '{}' and password='{}'".format(usrid,pwd))][0][0]:
      session['name'] = usrid
      return "Data Found"
    else:
      return "Not Found"

# SignUp
@app.route('/addUser/<value>',methods=['POST'])
def addUser(value):
  usr,mail,pwd,usrid = value.split('-_-')
  conn = sqlite3.connect('data.db')
  if request.method == 'POST':
    file = request.files['file']
    if file:
      filename = secure_filename(file.filename)
      filename = usrid+'.'+filename.rsplit('.', 1)[1].lower()
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      conn.execute('insert into user(usrid,usr ,mailid,password,url)values(?,?,?,?,?)',(usrid,usr,mail,pwd,'/static/./UserPics/'+filename))
      conn.commit()
  return "True"
  
# CheckUser
@app.route('/checkUser/<value>',methods=['POST'])
def checkUser(value):
  conn =  sqlite3.connect('data.db')
  
  return str(len([i for i in conn.execute("select count(*) from user where usrid = '{}'".format(value))]))

  
# CheckMail
@app.route('/checkMail/<value>',methods=['POST'])
def checkMail(value):
  conn = sqlite3.connect('data.db')
  return str(len([i for i in conn.execute("select count(*) from user where mailid='{}'".format(value))]))
conn = sqlite3.connect('data.db')
for i in conn.execute('select * from user'):
  print(i)


# iptracker


@app.route('/ip_tracker', methods=['GET', 'POST'])
def ip_tracker():
    val,loc,usrname = readData(frm='main')
    ip_details = None
    if request.method == 'POST':
        ipurl = request.form.get('ip_address')
        ip=url_to_ip(ipurl)
        ip_details = ip_address_tracker(ip)
    return render_template('ip_tracker.html', ip_details=ip_details,loc=loc)

@app.route('/usr_pass', methods=['GET', 'POST'])
def usr_pass():
    val,loc,usrname = readData(frm='main')
    message = None
    sources = None
    if request.method == 'POST':
        username = request.form.get('Username')
        # username = request.form['username']
        password = request.form.get('password')

        result2 = is_username_leaked(username)
        result = check_password_strength(password)
        count = pwned_api_check(password)
        
        
        if count:
               result1 = f'\"{ password }\"  is found  {count}  times. You should change it'
               message = result2['message']
               sources = result2.get('sources', [])
               return render_template('usr_pass.html', result=result,result1=result1,loc=loc,count=count,checked=True,message=message, sources=sources)
        else:
               result1= f"\"{ password }\" is not  found. You're good to go"
               message = result2['message']
               sources = result2.get('sources', [])
               return render_template('usr_pass.html', result=result,result1=result1,loc=loc,checked=True,message=message, sources=sources)
    return render_template('usr_pass.html',loc=loc)



@app.route('/website_scanner', methods=['GET', 'POST'])
def website_scanner():
    val,loc,usrname = readData(frm='main')

    analysis_results = None  # Set analysis_results to None by default
    
    if request.method == 'POST':
        url = request.form.get('url')
        analysis_results = analyze_website(url)  # Update analysis_results if URL is provided
    
    return render_template('website_scanner.html', results=analysis_results,loc=loc)

@app.route('/bv_scanner', methods=['GET', 'POST'])
def bv_scanner():
    val,loc,usrname = readData(frm='main')

    if request.method == 'POST':
        url = request.form['url']
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url  # Add 'https://' prefix if not present
        # Ensure URL ends with '/'
        if not url.endswith('/'):
            url += '/'
            clickjacking_status = clickjacking_scan(url)
            xss_status = xss_scan(url)
            sql_injection_status = sql_injection_scan(url)
            rce_status = rce_scan(url)
            csrf_status = csrf_scan(url)
            lfi_status = lfi_scan(url)


            vulnerabilities = [
              {"type": "Clickjacking", "status": clickjacking_status},
              {"type": "XSS", "status": xss_status},
              {"type": "SQL Injection", "status": sql_injection_status},
              {"type": "RCE", "status": rce_status},
              {"type": "CSRF", "status": csrf_status},
              {"type": "LFI", "status": lfi_status}
          ]

        return render_template('basic_vuln.html', url=url, vulnerabilities=vulnerabilities,loc=loc)
    else:
        return render_template('basic_vuln.html',loc=loc)
    



    # picsure


@app.route('/picsure', methods=['GET', 'POST'])
def upload_and_compare():
    val,loc,usrname = readData(frm='main')

    if request.method == 'POST':
        # Get the uploaded images
        image1 = request.files['image1']
        image2 = request.files['image2']
        # image2 = request.files['image2']
        # Save the images to the local directory
        image1.save('static/img/image1.png')
        image2.save('static/img/image2.png')
        image1.save('image1.png')
        image2.save('image2.png')



    
        # Load the image
        image = cv2.imread('static/img/image1.png')
        topleftimg,bottomrightimg=divide_image(image)
        halfbinary1= cv2.imencode('.png',topleftimg)[1].tobytes().hex()
        halfbinary2= cv2.imencode('.png',bottomrightimg)[1].tobytes().hex()


        zero_count=count_zeros(halfbinary1)
        ones_count=count_ones(halfbinary2)

        
    

        # Compare the number of pixels
        pixels_image1 = get_pixel_count('static/img/image1.png')
        pixels_image2 = get_pixel_count('static/img/image2.png')




        if pixels_image1 == pixels_image2:
           resultp = 1
        else:
           resultp = -1


        # Read the image files
        img1 = Image.open(image1)
        img2 = Image.open(image2)

        im1 = Image.open('static/img/image1.png')
        im2 = Image.open('static/img/image2.png')

         
        # Compare the metadata of the images
        is_same_metadata = compare_metadata(img1, img2)


        # Convert images to binary
        binary1 = image_to_binary(img1)
        binary2 = image_to_binary(img2)


        zero_countfull= count_zerosfull(binary1)
        refid=zero_count+(pixels_image1-zero_countfull)-ones_count

        

        # Compare the binary codes
        binary_comparison = compare_binary(binary1, binary2)

        # Calculate the hash values
        hash1 = calculate_hash(binary1)
        hash2 = calculate_hash(binary2)

        # Compare the hash values
        hash_comparison = compare_hashes(hash1, hash2)

        # Determine the overall result
        if binary_comparison == 1 and hash_comparison == 1 and resultp==1 :
            return render_template('picsure.html',result=True,image1=image1, image2=image2, is_same_metadata=is_same_metadata,refid=refid,loc=loc) 
        else:

            return render_template('picsure.html',result=False, image1=image1, image2=image2, is_same_metadata=is_same_metadata,loc=loc)

        

    return render_template('picsure.html',loc=loc)

@app.route('/search', methods=['GET', 'POST'])
def search():
    val,loc,usrname = readData(frm='main')

    if request.method == 'POST':
        # Get the uploaded image and text input
        image = request.files['image']
        text = request.form['text']

        text=int(text)

        # Save the image to the local directory
        image.save('static/img/search_image.png')

               
        image1 = cv2.imread('static/img/search_image.png')

        topleftimg,bottomrightimg=divide_image(image1)
        halfbinary1= cv2.imencode('.png',topleftimg)[1].tobytes().hex()
        halfbinary2= cv2.imencode('.png',bottomrightimg)[1].tobytes().hex()
        

        zero_count=count_zeros(halfbinary1)
        ones_count=count_ones(halfbinary2)
        pixels_image1 = get_pixel_count('static/img/search_image.png')
        img1 = Image.open(image)
        binary1 = image_to_binary(img1)
        zero_countfull= count_zerosfull(binary1)
        refid=zero_count+(pixels_image1-zero_countfull)-ones_count
        refid=int(refid)
        if text== refid :
            return render_template('picsure.html', result1=True, refid=refid,text=text,loc=loc) 
        else:

            return render_template('picsure.html',result1=False, text=text,loc=loc) 

    return render_template('picsure.html')


def image_to_binary(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def compare_binary(binary1, binary2):
    return 1 if binary1 == binary2 else -1

def calculate_hash(binary):
    return hashlib.sha256(binary).hexdigest()

def compare_hashes(hash1, hash2):
    return 1 if hash1 == hash2 else -1

def get_pixel_count(image_path):
    with open(image_path, 'rb') as file:
        file.seek(2)  # Skip the first two bytes (signature)
        width = int.from_bytes(file.read(4), 'big')
        height = int.from_bytes(file.read(4), 'big')
        return width * height
    
def compare_metadata(image1, image2):
          metadata1 = image1._getexif()
          metadata2 = image2._getexif()

          return 1 if metadata1 == metadata2 else -1
def divide_image(image):
    # Get the dimensions of the image
        height, width, _ = image.shape

        # Divide the image into four equal parts
        half_height = height // 2
        half_width = width // 2

        top_left = image[:half_height, :half_width]
        top_right = image[:half_height, half_width:]
        bottom_left = image[half_height:, :half_width]
        bottom_right = image[half_height:, half_width:]

        return top_left,bottom_right

def count_zeros(halfbinary):
        count = 0
        for bit in halfbinary:
           if bit == '0':
             count += 1
        return count
def count_zerosfull(fullbinary):
        count = 0
        for bit in fullbinary:
           if bit == '0':
             count += 1
        return count
def count_ones(fullbinary):
        count = 0
        for bit in fullbinary:
           if bit == '1':
             count += 1
        return count





        # report







@app.route('/adv_scan', methods=['GET', 'POST'])
def adv_scan():
    val,loc,usrname = readData(frm='main')

    message = None
    sources = None
    text_tags=None
    scan_result = None
    strength=count=None
    ip_details=None
    analysis_results = None
    vulnerabilities=None
    if request.method == 'POST':
        url = request.form['url']
        username = request.form['username']
        password=request.form['password']
        strength = check_password_strength(password)
        count = pwned_api_check(password)
        result = is_username_leaked(username)
        ipurl=clean_url(url)
        ip=url_to_ip(ipurl)
        ip_details = ip_address_tracker(ip)
        analysis_results = analyze_website(url)
        if 'error' in result:
            message = result['error']
        else:
            message = result['message']
            sources = result.get('sources', [])

        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url  # Add 'https://' prefix if not present
        # Ensure URL ends with '/'
        if not url.endswith('/'):
            url += '/'
            text_tags = crawl_and_extract(url)
            scan_result = scan_url1(url)

            clickjacking_status = clickjacking_scan(url)
            xss_status = xss_scan(url)
            sql_injection_status = sql_injection_scan(url)
            rce_status = rce_scan(url)
            csrf_status = csrf_scan(url)
            lfi_status = lfi_scan(url)


            vulnerabilities = [
              {"type": "Clickjacking", "status": clickjacking_status},
              {"type": "XSS", "status": xss_status},
              {"type": "SQL Injection", "status": sql_injection_status},
              {"type": "RCE", "status": rce_status},
              {"type": "CSRF", "status": csrf_status},
              {"type": "LFI", "status": lfi_status}
          ]
    return render_template('adv_scan.html',loc=loc,text_tags=text_tags, scan_result=scan_result, message=message, sources=sources,strength=strength,count=count,ip_details=ip_details,results=analysis_results,vulnerabilities=vulnerabilities)

if __name__ == "__main__":
    app.run(debug=True)