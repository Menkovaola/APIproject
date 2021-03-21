from db import db
import sqlite3 as lite


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name, user_id):
        return cls.query.filter_by(name=name, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, id, user_id):
        return cls.query.filter_by(id=id, user_id=user_id).first()

    @classmethod
    def find_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def delete_from_db(cls, id, user_id):
        con = lite.connect('object-collection.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM items where id = ? and user_id = ?", (id, user_id))
            row = cur.fetchone()
            if row:
                cur.execute("DELETE FROM items where id = ? and user_id = ?", (id, user_id))
                return 'true'
            else:
                return 'false'

    @classmethod
    def transfer(cls, id, user_id):
        con = lite.connect('object-collection.db')

        with con:
            cur = con.cursor()
            try:
                cur.execute("UPDATE items SET user_id = ? WHERE id = ?",
                            (user_id, id))
            except:
                return 'error'