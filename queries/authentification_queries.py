from flask import Flask
from flask import g
import sqlite3

DATABASE = 'bdd/oopshunter.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def check_login(mail,password) :
    c = get_db().cursor()
    login = c.execute("SELECT * FROM EMPLOYEE WHERE mail = ? AND password = ?", (mail, password)).fetchone()
    if login is None : 
        return None
    else : 
        return login[0]

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()