import sqlite3 as lite

from db import db
from datetime import datetime


class TokenModel(db.Model):
    __tablename__ = 'tokens'
    token = db.Column(db.String(80), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    @classmethod
    def save_to_db(cls, token, user_id):
        con = lite.connect('object-collection.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM tokens where user_id = ?", [user_id])
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                cur.execute("INSERT INTO tokens VALUES(?,?)", (token, user_id))
                return token

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()
