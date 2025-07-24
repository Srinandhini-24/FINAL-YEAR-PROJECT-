from flask import Flask, render_template, flash, request,session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import secure_filename
import mysql.connector
import urllib
import urllib.request
import urllib.parse
import string
import hashlib
import base64
import os
from io import BytesIO
import datetime
import yagmail


import tkinter.messagebox
#import os, shutil

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])


class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"

class Blockchain:

    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1

#blockchain = Blockchain()
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])





@app.route("/")
def homepage():

    return render_template('login.html')

@app.route("/viewrq")
def viewrq():
    n = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
    cursor = conn.cursor()
    cursor.execute("SELECT * from share1 where uname='" + n + "' and status='2'")
    data = cursor.fetchall()


    return render_template('viewrq.html',data=data)



@app.route("/reg")
def reg():

    return render_template('register.html')
@app.route("/profile")
def profile():

    return render_template('profile.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        n = request.form['name']

        # g = request.form['city']
        # st = request.form['station']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['pnumber']
        uname = request.form['uname']
        password = request.form['password']
        mydb = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = mydb.cursor()
        mycursor = mydb.cursor()

        mycursor.execute("select max(id) from register")

        myresult = mycursor.fetchall()

        for x in myresult:
            y = x[0]
            break
        if y == None:
            print("No such charater available in string")
            x1=1
        else:
            y1 = y
            x1 =int(y1)+1

        cursor.execute(
            "INSERT INTO register VALUES ('"+str(x1)+"','" + n + "','" + address + "','" + email + "','" + pnumber + "','" + uname + "','" + password + "','0','0','0','0')")

        mycursor1 = mydb.cursor()
        mycursor1.execute("select * from register where id!='"+str(x1)+"'")
        myresult1 = mycursor1.fetchall()
        for z in myresult1:
            frid=z[0]
            fname=z[1]
            mycursor2 = mydb.cursor()
            mycursor2.execute("insert into frlist(id,name,mailid,frid,frname,status)values('"+str(x1)+"','"+n+"','','"+str(frid)+"','"+str(fname)+"','0')")
            mycursor2 = mydb.cursor()
            mycursor2.execute("insert into frlist(id,name,mailid,frid,frname,status)values('" + str(frid) + "','" + str(fname) + "','','" + str(x1) + "','" + n + "','0')")
            #rt="http://bulksms.mysmsmantra.com:8080/WebSMS/SMSAPI.jsp?username=username&password=password&sendername=sender id&mobileno=919999999999&message=Hello"
        mydb.commit()
        mydb.close()

        return render_template('login.html',data=myresult1,data1=myresult)

@app.route("/login",methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':

        n = request.form['uname']
        session['uname'] = request.form['uname']
        g = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where uname='" + n + "' and password='" + g + "' and ot='0'")
        data = cursor.fetchone()

        if data is None:
            return 'Username or Password is wrong'
        else:
            cursor1 = conn.cursor()
            cursor1.execute("SELECT * from register where uname='" + n + "' and password='" + g + "' and ot='0'")
            data1=cursor1.fetchall()
            for x in data1:
                pnumber=x[4]
                usid=x[0]
            session['userid'] = usid
            import random
            for i in range(1):
                n1 = random.randrange(100000, 900000)
            flash("Logged in successfully.")
            ph = pnumber
            msg = str(n1)


            # return 'file uploaded successfully'
            return render_template('home.html',uname=session['uname'])
@app.route("/home")
def userhome():
    n = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
    cursor = conn.cursor()
    cursor.execute("SELECT * from register where uname='" + n + "'")
    data = cursor.fetchall()

    for x in data:
        uid = x[0]
        d=x[1]
        i=x[9]

    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor = mydb.cursor()

    mycursor.execute("select * from upost where sid='" + str(uid) + "'")
    data1 = mycursor.fetchall()
    mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor1 = mydb1.cursor()
    mycursor1.execute("SELECT upost.sid, upost.image, upost.cption,upost.date,upost.time, frlist.id, frlist.frname,upost.id  FROM  upost INNER JOIN frlist  ON upost.sid = frlist.frid WHERE  frlist.id = '"+str(uid)+"' and frlist.status = '2'")
    upost = mycursor1.fetchall()

    return render_template('home.html',data=data1,data1=d,data2=i,upost=upost,uname=session['uname'])
@app.route("/list")
def list():
    n = session['uname']
    my_list = []

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
    cursor = conn.cursor()
    cursor.execute("SELECT * from register where uname='" + n + "'")
    data = cursor.fetchall()
    for x in data:
        uid=x[0]

    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor = mydb.cursor()

    mycursor.execute("select * from frlist where id='"+str(uid)+"' && status='0'")
    data1 = mycursor.fetchall()
    for x1 in data1:
       frid=str(x1[3])

       mycursor1 = mydb.cursor()

       mycursor1.execute("select * from register where id='" + str(frid) + "'")
       data2 = mycursor1.fetchall()
       for f in data2:


        fs=str(f[9])

        my_list.append(f[9])




    return render_template('list.html',data=data1,data2=my_list,len = len(my_list),uname=session['uname'])
@app.route("/frlist")
def frlist():
    n = session['uname']

    mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor1 = mydb1.cursor()

    mycursor1.execute("select * from frlist where name='" + str(n) + "' && status='2'")
    data2 = mycursor1.fetchone()
    if data2 is None:
        return render_template('frlist.html',uname=session['uname'])
    else:
        aList = []

        mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor1 = mydb1.cursor()

        mycursor1.execute("select * from frlist where name='" + str(n) + "' && status='2'")
        data2 = mycursor1.fetchall()
        for x1 in data2:
            frid = str(x1[3])

            mycursor11 = mydb1.cursor()

            mycursor11.execute("select * from register where id='" + frid + "'")
            data22 = mycursor11.fetchall()
            for v in data22:

                aList.append(v[1])


        d = aList


        return render_template('frlist.html', data1=data22,uname=session['uname'])


@app.route("/post")
def post():




    return render_template('post.html',uname=session['uname'])
@app.route("/accept")
def accept():
    n = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
    cursor = conn.cursor()
    cursor.execute("SELECT * from register where uname='" + n + "'")
    data = cursor.fetchall()
    for x in data:
        uid = x[0]

    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor = mydb.cursor()

    mycursor.execute("select * from frlist where frid='" + str(uid) + "' && status='1'")
    data1 = mycursor.fetchone()
    if data1 is None:
        return render_template('accept.html',uname=session['uname'])
    else:
        aList = []
        mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor1 = mydb1.cursor()

        mycursor1.execute("select * from frlist where frid='" + str(uid) + "' && status='1'")
        data2 = mycursor1.fetchall()
        for x1 in data2:
            frid = str(x1[0])

            mycursor11 = mydb1.cursor()

            mycursor11.execute("SELECT register.id, register.name, register.image FROM register INNER JOIN frlist ON register.id=frlist.id WHERE (frlist.frid ='"+str(uid)+"' && frlist.status='1')  && register.id!='"+str(uid)+"'")
            data22 = mycursor11.fetchall()
            for v in data22:

                aList.append(v[1])


        d=aList



        return render_template('accept.html', data=data2, data1=data22,uname=session['uname'])

@app.route("/accept1",methods = ['GET'])
def accept1():

        n = request.args.get('act')
        id=request.args.get('id')
        n1 = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where uname='" + n1 + "'")
        data = cursor.fetchall()
        for x in data:
            uid = x[0]
        if n=="snt":

            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor = mydb.cursor()

            mycursor.execute("update frlist set status='2' where id='" + str(uid)+ "' and frid='" + id + "'")
            mydb.commit()
            mydb.close()
            mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor1 = mydb1.cursor()

            mycursor1.execute("update frlist set status='2' where frid='" + str(uid) + "' and id='" + id + "'")
            mydb1.commit()
            mydb1.close()
            return render_template('home.html')
        if n=="rejt":
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor = mydb.cursor()

            mycursor.execute("update frlist set status='3' where id='" + str(uid) + "' and frid='" + id + "'")
            mydb.commit()
            mydb.close()
            mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor1 = mydb1.cursor()

            mycursor1.execute("update frlist set status='3' where frid='" + str(uid) + "' and id='" + id + "'")
            mydb1.commit()
            mydb1.close()
            return render_template('home.html',uname=session['uname'])

@app.route("/notification")
def notification():
    uid=session['userid']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
    cursor = conn.cursor()
    cursor.execute("SELECT upost.id,comment.id,comment.uname,comment.cmt FROM upost INNER JOIN comment ON upost.id = comment.mid WHERE  upost.sid = '"+str(uid)+"' and comment.status='1'")
    data = cursor.fetchall()

    conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
    cursor11 = conn11.cursor()
    cursor11.execute(
        "SELECT upost.id,upost.image,upost.cption,share.uname FROM upost INNER JOIN share ON upost.id = share.mid WHERE  upost.sid = '" + str(
            uid) + "' and share.status='1'")
    data1 = cursor11.fetchall()

    "SELECT upost.id FROM upost INNER JOIN comment ON upost.id = comment.mid WHERE  upost.sid = '2' and comment.status='1'"

    return render_template('notification.html',data=data,data1=data1,uname=session['uname'])
@app.route("/commt")
def commt():


    return render_template('commt.html')
@app.route("/login1",methods = ['GET', 'POST'])
def login1():

    if request.method == 'POST':
        n = request.form['uname']
        name=session['uname']
        #g = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where uname='" + name + "' and ot='" + n + "'")
        data = cursor.fetchone()

        if data is None:
            return 'Username or Password is wrong'
        else:



            return render_template('home.html',uname=session['uname'])
@app.route("/list1",methods = ['GET'])
def list1():


        n = request.args.get('act')

        g = request.args.get('id')
        name = session['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()
        cursor.execute("select * from register where uname='"+name+"'")
        data=cursor.fetchall()
        for x1 in data:
           uid=str(x1[0])

        mydb3 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor3 = mydb3.cursor()

        mycursor3.execute("select * from  frlist  where id='" + str(uid) + "' && frid='" + str(g) + "' && status='0'")
        data=mycursor3.fetchone()
        if data is None:
           print("data")


        else:
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor = mydb.cursor()

            mycursor.execute("update frlist set status='1' where id='" + str(uid) + "' && frid='" + str(g) + "'")
            mydb.commit()
            mydb.close()
            mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor1 = mydb1.cursor()

            mycursor1.execute("update frlist set status='0' where id='" + str(g) + "' && frid='" + str(uid) + "'")
            mydb1.commit()
            mydb1.close()

            mydb4 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor4 = mydb4.cursor()

            mycursor4.execute("select * from frlist where id='" + str(uid) + "' && status='0'")
            data1 = mycursor4.fetchall()
            return render_template('list.html',data=data1,uname=session['uname'])



@app.route("/profile1",methods = ['GET', 'POST'])
def profile1():

    if request.method == 'POST':
        dob = request.form['dob']
        n = request.form['name']
        Work=request.form['work']
        place=request.form['from']
        f = request.files['file']
        f.save("static/uploads/" + secure_filename(f.filename))
        name=session['uname']
        #g = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()
        cursor.execute("select * from register where uname='" + name + "'")
        data = cursor.fetchall()
        for x1 in data:
            uid = str(x1[0])

        mycursor = conn.cursor()

        mycursor.execute("update register set dob='"+dob+"',work='"+Work+"',image='"+f.filename+"' where id='" + str(uid) +"'")
        conn.commit()
        conn.close()
        return render_template('home.html',uname=session['uname'])

@app.route("/post1",methods = ['GET', 'POST'])
def post1():
    if request.method == 'POST':

        place=request.form['caption']
        f = request.files['file']
        f.save("static/uploads/" + secure_filename(f.filename))
        name=session['uname']
        from stegano import lsb
        clear_message = lsb.reveal("static/uploads/" + secure_filename(f.filename))
        print(clear_message)
        if clear_message=="None":
            mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor1 = mydb1.cursor()

            mycursor1.execute("select * from register where uname='" + str(name) + "'")
            d1 = mycursor1.fetchall()
            for x1 in d1:
                im = str(x1[9])

            # Import required Image library
            # Import required Image library
            from PIL import Image, ImageFilter

            # Open existing image
            OriImage = Image.open("static/uploads/" + f.filename)
            # OriImage.show()

            # Applying GaussianBlur filter
            gaussImage = OriImage.filter(ImageFilter.GaussianBlur(5))
            # gaussImage.show()

            # Save Gaussian Blur Image
            gaussImage.save("static/upload/" + f.filename)
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
            cursor = conn.cursor()
            cursor.execute("select * from register where uname='" + name + "'")
            data = cursor.fetchall()
            for x1 in data:
                uid = str(x1[0])

            mycursor = conn.cursor()

            mycursor.execute(
                "insert into upost values('','" + uid + "','" + f.filename + "','" + place + "','','0','" + name + "','" + im + "','0','')")
            conn.commit()
            conn.close()
            return render_template('home.html', uname=session['uname'])
        else:
            mconn = mysql.connector.connect(host="localhost", user="root", password="", database="newfacebook")
            mc = mconn.cursor()
            mc.execute("select * from register where name='" + str(clear_message) + "'")
            m = mc.fetchone()
            email = m[3]
            mail = 'testsam360@gmail.com';
            password = 'rddwmbynfcbgpywf';
            # list of email_id to send the mail
            li = [email]
            body = "warning Your post Photo Useing Other Social Media Platform"
            yag = yagmail.SMTP(mail, password)
            yag.send(to=email, subject="Alert...!", contents=body)

            
            return render_template('home.html', uname=session['uname'])

@app.route("/cmt",methods = ['GET'])
def cmt():
    n = request.args.get('act')
    id = request.args.get('id')
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor = mydb.cursor()

    mycursor.execute("select * from upost where id='" + str(id) + "'")
    data1 = mycursor.fetchall()
    for item in data1:
        pid=item[1]
        pname=item[3]

    mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor1 = mydb1.cursor()

    mycursor1.execute("select * from register where id='"+str(pid)+"'")
    d1 = mycursor1.fetchall()

    for d in d1:
        rimg=d[9]
        rname=d[1]
    mydb11 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
    mycursor11 = mydb11.cursor()
    mycursor11.execute("select * from comment where mid='" + str(id) + "'  and status='0'")
    d11 = mycursor11.fetchall()





    "SELECT upost.sid, upost.image, upost.cption, frlist.id, frlist.name  FROM  upost INNER JOIN frlist  ON upost.sid = frlist.frid WHERE  frlist.id = '1' and frlist.status = '2'"

    return render_template('commt.html',data=data1,data11=rimg,data111=rname,cm=d11,uname=session['uname'])
@app.route("/cmmt",methods = ['GET', 'POST'])
def cmmt():
    if request.method == 'POST':
        commt = request.form['commt']
        uid = session['userid']
        un=session['uname']
        pid=request.form['pid']
        mydb11 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor11 = mydb11.cursor()
        mycursor11.execute("select * from comment where mid='" + str(pid) + "'  and status='0'")
        d11 = mycursor11.fetchall()

        d = ["careless", "together", "criminal", "corrupt", "depressed", "Overcritical", "Aggressive", "Armchair",
             "critic", "Cynical", "Impulsive", "Tactless", "Thoughtless", "badmood", "hurtful", "lose",
             "lousy", "lumpy", "naive", "nasty", "naughty", "negate", "negative", "never", "nobody", "non",
             "descript", "noxious", "sad", "stupid", "stressful", "upset", "worthless", "zero", "ugly", "undermine",
             "unfair", "unfavorable", "unhappy", "unhealthy", "not+good"]
        fruits = []
        fruits.append(commt)
        sentence1 = fruits

        def check_all(sentence1, ws):
            return all(w in sentence1 for w in ws)

        for sentences in sentence1:
            if any(check_all(sentences, word.split('+')) for word in d):

                sta = 1
                ts=1
                break
            else:

                print('not fount')
                sta = 0
                ts=0
                break

        import datetime
        from datetime import datetime
        now = datetime.now()

        date = now.strftime("%m/%d/%Y")

        time = now.strftime("%H:%M:%S")

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        #cursor = conn.cursor()
        mycursor = conn.cursor()




        mycursor.execute("insert into comment values('','"+str(pid)+"','"+str(uid)+"','"+str(un)+"','"+str(commt)+"','"+str(sta)+"','"+str(ts)+"','"+str(date)+"','"+str(time)+"')")
        conn.commit()
        conn.close()

        # ================================================================mail===================================

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()
        cursor.execute("SELECT sum(csta) as count  FROM comment WHERE uname  ='" + str(un) + "'")
        data2 = cursor.fetchone()
        if data2:
            ccount = data2[0]

        else:
            print('no data')

        if (ccount == 1):
            mconn = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mc = mconn.cursor()
            mc.execute("select * from register where id='" + str(uid) + "'")
            m = mc.fetchone()
            email = m[3]
            mail = 'testsam360@gmail.com';
            password = 'rddwmbynfcbgpywf';
            # list of email_id to send the mail
            li = [email]
            body = "warning unwanted comments to this post"
            yag = yagmail.SMTP(mail, password)
            yag.send(to=email, subject="Alert...!", contents=body)
        elif (ccount == 2):
            mconn = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mc = mconn.cursor()
            mc.execute("select * from register where id='" + str(uid) + "'")
            m = mc.fetchone()
            email = m[3]
            mail = 'testsam360@gmail.com';
            password = 'rddwmbynfcbgpywf';
            # list of email_id to send the mail
            li = [email]
            body = "You Have one More Time Give unwanted comment"
            yag = yagmail.SMTP(mail, password)
            yag.send(to=email, subject="Alert...!", contents=body)



        elif (ccount > 3):

            mconn = mysql.connector.connect(host="localhost", user="root", password="", database="newnewtwitter")
            mc = mconn.cursor()
            mc.execute("select * from register where id='" + str(uid) + "'")
            m = mc.fetchone()
            email = m[3]
            mail = 'testsam360@gmail.com';
            password = 'rddwmbynfcbgpywf';
            # list of email_id to send the mail
            li = [email]
            body = "You are Block "
            yag = yagmail.SMTP(mail, password)
            yag.send(to=email, subject="Alert...!", contents=body)
            mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
            mycursor1 = mydb1.cursor()
            mycursor1.execute("update register set status='Blocked' where id='" + str(uid) + "'")
            mydb1.commit()
            mydb1.close()

        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor = mydb.cursor()

        mycursor.execute("select * from upost where id='" + str(pid) + "'")
        data1 = mycursor.fetchall()
        for item in data1:
            pid = item[1]
            pname = item[3]

        mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor1 = mydb1.cursor()

        mycursor1.execute("select * from register where id='" + str(pid) + "'")
        d1 = mycursor1.fetchall()

        for d in d1:
            rimg = d[9]
            rname = d[1]
        "SELECT upost.sid, upost.image, upost.cption, frlist.id, frlist.name  FROM  upost INNER JOIN frlist  ON upost.sid = frlist.frid WHERE  frlist.id = '1' and frlist.status = '2'"
        mydb11 = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor11 = mydb11.cursor()
        mycursor11.execute("select * from comment where mid='" + str(pid) + "'  and status='0'")
        d11 = mycursor11.fetchall()


        return render_template('commt.html',data=data1,data11=rimg,data111=rname,cm=d11,uname=session['uname'])
@app.route("/notification1",methods = ['GET'])
def notification1():

        n = request.args.get('act')
        id=request.args.get('id')
        uid=session['userid']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()

        mycursor = conn.cursor()

        mycursor.execute("update comment set status='0' where id='"+id+"'")
        conn.commit()
        conn.close()
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor1 = conn1.cursor()
        cursor1.execute(
            "SELECT upost.id,comment.id,comment.uname,comment.cmt FROM upost INNER JOIN comment ON upost.id = comment.mid WHERE  upost.sid = '" + str(
                uid) + "' and comment.status='1'")
        data = cursor1.fetchall()

        conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor11 = conn11.cursor()
        cursor11.execute(
            "SELECT upost.id,upost.image,upost.cption FROM upost INNER JOIN share ON upost.id = share.mid WHERE  upost.sid = '" + str(
                uid) + "' and share.status='1'")
        data1 = cursor11.fetchall()

        print('data')



        return render_template('notification.html', data=data, data1=data1,uname=session['uname'])
@app.route("/share",methods = ['GET'])
def share():

        n = request.args.get('act')
        id=request.args.get('id')
        uid=session['userid']
        uname=session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()

        mycursor = conn.cursor()

        mycursor.execute("insert into share values('','"+str(id)+"','"+str(uid)+"','1','"+uname+"')")
        conn.commit()
        conn.close()

        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="newtwitter")
        mycursor = mydb.cursor()

        mycursor.execute("select * from upost where id='" + str(id) + "'")
        data1 = mycursor.fetchall()
        for item in data1:
            pid = item[1]
            pname = item[2]
        txt = pname

        x = txt.split(".")
        fn = x[0]
        img=str(fn)+".png"


        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor1 = conn1.cursor()

        mycursor1 = conn1.cursor()

        mycursor1.execute("insert into share1 values('','" + str(id) + "','" + str(uid) + "','1','" + uname + "','"+img+"')")
        conn1.commit()
        conn1.close()
        return render_template('home.html',uname=session['uname'])

@app.route("/share1",methods = ['GET'])
def share1():

        n = request.args.get('act')
        id=request.args.get('id')
        uid=session['userid']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()

        mycursor = conn.cursor()

        mycursor.execute("update share set status='2' where mid='"+id+"'")
        conn.commit()
        conn.close()
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor1 = conn1.cursor()
        cursor1.execute(
            "SELECT upost.id,comment.id,comment.uname,comment.cmt FROM upost INNER JOIN comment ON upost.id = comment.mid WHERE  upost.sid = '" + str(
                uid) + "' and comment.status='1'")
        data = cursor1.fetchall()

        conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor11 = conn11.cursor()
        cursor11.execute(
            "SELECT upost.id,upost.image,upost.cption FROM upost INNER JOIN share ON upost.id = share.mid WHERE  upost.sid = '" + str(
                uid) + "' and share.status='1'")
        data1 = cursor11.fetchall()

        print('data')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='newtwitter')
        cursor = conn.cursor()

        mycursor = conn.cursor()

        mycursor.execute("update share1 set status='2' where mid='" + id + "'")
        conn.commit()
        conn.close()

        return render_template('notification.html', data=data, data1=data1,uname=session['uname'])
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)