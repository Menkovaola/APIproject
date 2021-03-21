import sqlite3 as lite

from db import db


class TransferModel(db.Model):
    __tablename__ = 'transfer'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    items = db.relationship('ItemModel')

    def __init__(self, item_id, user_id):
        self.user_id = user_id
        self.item_id = item_id

    @classmethod
    def save_to_db(cls, user_id, item_id):
        con = lite.connect('object-collection.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM transfer where item_id = ?", [item_id])
            row = cur.fetchone()
            if row:
                return "true"
            else:
                cur.execute("INSERT INTO transfer VALUES(?,?)", (user_id, item_id))
                return "false"

    @classmethod
    def find_transfer(cls, user_id, item_id):
        return cls.query.filter_by(user_id=user_id,item_id=item_id).first()

    @classmethod
    def delete_transfer(cls, user_id, item_id):
        con = lite.connect('object-collection.db')

        with con:
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM transfer WHERE user_id = ? and item_id = ?", (user_id,item_id))
            except:
                return 'error'
