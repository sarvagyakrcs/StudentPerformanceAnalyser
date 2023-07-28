from sqlalchemy import create_engine, Column, String, CHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
import hashlib

import os
import MySQLdb

connection = MySQLdb.connect(
  host= os.getenv("HOST"),
  user=os.getenv("USERNAME"),
  passwd= os.getenv("PASSWORD"),
  db= os.getenv("DATABASE"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/cert.pem"
  }
)


class User(Base):
    __tablename__ = 'users'

    email = Column(String(255), primary_key=True)
    password = Column(String(255))
    accountType = Column(CHAR(1))


Session = sessionmaker(bind=engine)
session = Session()


def verifyLogin(email, password):
    user = session.query(User).filter_by(email=email).first()
    print(user)
    if user:
        if (user.password == hashlib.sha256(password.encode()).hexdigest()):
            return True
        return False
    return False


def verifyAccountCreation(email, password, confirmPassword):
    if confirmPassword != password:
        return "Passwords dont match!"
    user = session.query(User).filter_by(email=email).first()

    if user:
        return "Account already exists"

    new_user = User(email=email, password=hashlib.sha256(password.encode()).hexdigest(), accountType='A')
    session.add(new_user)
    session.commit()
    return None




