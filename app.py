import models,os, json, csv, requests,sys, random,datetime
from flask import Flask, session,abort, redirect, render_template, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from flask_bootstrap import Bootstrap
from functools import wraps

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('configmodule.DevelopmentConfig')#ProductionConfig
Session(app)
engine = create_engine('postgres://jjftsdutfuwhhl:c773f8e072b7c4cbc5736ecc10b042961c11d0efe8a7b54aecfca685be041851@ec2-18-235-20-228.compute-1.amazonaws.com:5432/dbb5crinco6nc9')
db = scoped_session(sessionmaker(bind=engine))
cover="http://covers.openlibrary.org/b/isbn/9780385533225-S.jpg"
def login_required(f):
    """Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
def totalBooks(): return db.execute('select count(*) from books').fetchone()[0]
def goodreads(isbn):
    return requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qLNlxu8ER2cIdvCQbaZLDg", "isbns": isbn}).json()
@app.route("/", methods=["GET"])
@login_required
def index():
    s=random.randint(1, totalBooks())
    booktoshow=db.execute('select title, author, year,isbn,id from books').fetchall()[s:s+9]
    # print(booktoshow, file=sys.stderr)
    return render_template("index.html",totalBook='Total Books available: '+str(totalBooks())+ '  Here is 9 random book ;-)',bookList=booktoshow)
@app.route("/login", methods=["POST",'GET'])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("login.html",message='Please submit both username and password!') 
        username = str(request.form.get("username")).lower()
        passW=request.form.get("password")        
        user=db.execute("select * from users where username=:user",{'user':username}).fetchone()
        # print(user, file=sys.stderr)        
        if user==None:
            return render_template("register.html",message='Please Register as Your usernaem is not registered!') 
        elif not check_password_hash(user[2], str(passW)):
            return render_template("login.html",message='Please Check your password again!')  
        session["user_id"] = user[0]
        session["user_name"] = user[1].lower()
        return redirect("/")#render_template("index.html")
    else:
        return render_template("login.html")
@app.route('/register', methods=["POST",'GET'])
def register():
    session.clear()
    if request.method=='GET':
        return render_template("register.html",message='') 
    else:
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("register.html",message='Please submit both username and password!') 
        username = str(request.form.get("username")).lower()
        passW=request.form.get("password") 
        if db.execute("select username from users where username=:user",{'user':username}).rowcount>0:
            return render_template("register.html",message='Username is already token!')   
        elif passW!=request.form.get("confirmation"):
            return render_template("register.html",message='password is not match!')
        hashP = generate_password_hash(str(passW), method='pbkdf2:sha256', salt_length=8)
        user=db.execute("insert into users (username, password) VALUES (:user,:pass) RETURNING id",{'user':username.lower(),'pass':hashP})
        db.commit()
        flash('Account is Created', 'info')
        session["user_id"] = user.fetchone()[0]
        session["user_name"] = username
        return redirect("/")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/search", methods=["GET"])
@login_required
def search():
    if not request.args.get("book"):
        return render_template("index.html",totalBook='Total Books available: '+str(totalBooks()),error='Please Provide Some Entry First!')
    query=str(request.args.get("book")).strip().title()
    q='%'+query+'%'
    res=db.execute('select title, author, year,isbn,id from books where title like :query or author like :query or isbn like :query;',{"query": q})
    if res.rowcount==0:
        return render_template("index.html",totalBook='Total Books available: '+str(totalBooks()),bookList=[],query=request.args.get("book"))
    note='Your Search Returned '+ str(res.rowcount)+' results out of ' +str(totalBooks())+' Books Available'
    return render_template("index.html",totalBook=note,bookList=res.fetchmany(30),searchof='search result for '+str(query))
@app.route("/book/<int:b_id>", methods=["POST","GET"])
@login_required
def book(b_id):
    check=db.execute('select title, author, year,isbn,id from books where id= :query;',{"query": b_id})
    if check.rowcount==0:
        return render_template("index.html",totalBook='Total Books available: '+str(totalBooks()),error='Not Such a BOOK is found')
    if request.method=='POST':
        user=session["user_id"]
        comment=request.form.get('comment')      
        if len(comment.strip())==0:
            flash('No review was submitted! Rate and Review not accepted!', 'error')
            return redirect("/book/" + str(b_id))           
        checkR=db.execute('select * from comments where book_id= :b and user_id= :c;',{"b": b_id, 'c':user})
        if checkR.rowcount>0:
            flash('Multiple Reviews is not accepted!', 'error')
            return redirect("/book/" + str(b_id))             
        rate=request.form.get('rate')
        time=datetime.datetime.utcnow()
        db.execute("INSERT INTO comments (user_id,book_id,comment,rate,add_time) VALUES (:uID,:bID, :cmnt, :rte, :t);",
            {'uID':int(user),'bID':int(b_id),'cmnt':comment,'rte':rate, 't':time})
        db.commit()
        flash('Review submitted!', 'info')
    book=[{column: value for column, value in rowproxy.items()} for rowproxy in check][0]
    rating=goodreads(book['isbn'])
    if len(rating['books'])>0:
        temp=rating['books'][0]
    bookinfo={**book,**temp}
    rev=db.execute('select u.username, r.comment, r.add_time, r.rate from comments r inner join users u on r.user_id=u.id where r.book_id= :b order by add_time;',{"b": int(b_id)})
    if rev.rowcount>0:
        revw=[{column: value for column, value in rowproxy.items()} for rowproxy in rev]
    else:
        revw=None
    return render_template("book.html",bookInfo=bookinfo,reviews=revw)
@app.route('/api/<string:isbn>', methods=["GET"])
@login_required
def api(isbn):
    checkF=db.execute('select isbn from books where isbn=:qi;',{"qi": isbn.title()})
    if checkF.rowcount==0:
        abort(404, description="Book not found")
    check=db.execute('select b.title, b.author, b.year,b.isbn, count(c.id) as review_count, \
        avg(c.rate) as average_score from comments c right join books b on b.id= c.book_id \
        where b.isbn=:q group by b.isbn,b.title, b.author, b.year ;',{"q": str(isbn)})
    data=dict(check.fetchone())
    # data['average_score'] = float('%.2f'%(data['average_score']))
    if data['average_score']==None:
        data['average_score']= 0.0
    else:
        data['average_score']=float(str(data['average_score'])[:3])
    return jsonify(data)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404