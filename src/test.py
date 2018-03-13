from bid_db import db, bid, member

db.create_all()

bids = bid.query.all()
members = member.query.all()

for i in bids:
	print(i)

for t in members:
	print(t)