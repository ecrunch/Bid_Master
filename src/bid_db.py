from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/bid_test2.db'
db = SQLAlchemy(app)

class bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_name = db.Column(db.String(80), unique=True)
    total = db.Column(db.Integer, unique=False)
    members = db.relationship('member', backref='bid_member', lazy='dynamic')

    def __init__(self, bid_name, total):
        self.bid_name = bid_name
        self.total = total

    def __repr__(self):
        return '<test %r>' % self.bid_name + " " + int(self.total)

class member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(80), unique=False)
    bid_id = db.Column(db.Integer, db.ForeignKey('bid.id'))
    
    def __init__(self, member_name, bid_member):
        self.member_name = member_name
        self.bid_member = bid_member

    def __repr__(self):
        return '<member %r>' % self.member_name

class bid_table(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	room = db.Column(db.Integer, unique=False)
	price = db.Column(db.Integer, unique=False)
	owner = db.Column(db.String(80), unique=False)

	def __init__(self, room, price,owner):
		self.room = room
		self.price = price
		self.owner = owner
	def __repr__(self):
		return '<room %r>' % self.room + ' ' + self.price + ' ' + self.owner



