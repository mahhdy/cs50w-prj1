import os
from flask import Flask, render_template, request
import models
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgres://jjftsdutfuwhhl:c773f8e072b7c4cbc5736ecc10b042961c11d0efe8a7b54aecfca685be041851@ec2-18-235-20-228.compute-1.amazonaws.com:5432/dbb5crinco6nc9'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)
db.init_app(app)
def main():
    db.create_all()
if __name__=='__main__':
    with app.app_context():
        main()