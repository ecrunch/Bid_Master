from __future__ import print_function
import pandas as pd
from flask import Flask, render_template, request, jsonify, json
from src.algo import roompicker
from wtforms import Form
from wtforms import StringField, IntegerField
from .bid_db import db, bid, member
from pprint import pprint

app = Flask(__name__)

db.create_all()

bids = bid.query.all()
members = member.query.all()
rows = db.session.query(bid).count()

# start off with no exceptions
app.config['ROOMPICKER_EXCEPTION'] = ""

#create the form for entering bids
class BidForm(Form):
    # should verify that this is a y or an n TODO
    bid_bool = StringField('bool_choose')
    room_choice = IntegerField('room num')
    rent_choice = IntegerField('rent')

#this needs to be filled in by a form TODO
rp = roompicker.RoomPicker(roommates=['drew', 'casey', 'jepsen', 'joe', 'chris'], total_rent=4500,old = False,old_list=[],turn = 0)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # get the BidForm defined above
    bidform = BidForm(request.form)
    # if you hit go
    if request.method == 'POST':
        # and you chose "y" as bid_bool
        if bidform.bid_bool.data == 'y':
            # try to run the algo and reset the exception
            try:
                rp.run_algo(in_room_number=bidform.room_choice.data, in_bid=bidform.rent_choice.data)
                app.config['ROOMPICKER_EXCEPTION'] = ""
            # if it errors, set the exception so it can be printed to the page
            except Exception as e:
                app.config['ROOMPICKER_EXCEPTION'] = e
        # if you chose not to bid, pass that on to the algo
        else:
            # increment counter
            rp.pass_dude()
    # render the page
    return render_template('index.html', form=bidform,
                           html_data=rp.rooms_df.to_json(),
                           whos_up=rp.roommates[rp.turn],
                           myexcept = app.config['ROOMPICKER_EXCEPTION'])

# @app.route('/')
# def hello_world():
#   return render_template('index.html')

@app.route('/getAllData',methods=['POST'])
def getAllList():
    bids = bid.query.all()
    rows = db.session.query(bid).count()
    # try:
    dataList = []
    for i in range(0,rows):
        ms = member.query.filter(member.bid_member==bids[i])
        arr=[]
        for t in ms:
            arr.append(t.member_name)

        dataItem = {
            'id':bids[i].id
            ,'bid_name':bids[i].bid_name
            ,'total':bids[i].total
            ,'members':arr
            }
        dataList.append(dataItem)
        
    # except Exception as e:
    #     return str(e)
    # # pdb.set_trace()
    return json.dumps(dataList)

@app.route('/newData',methods=['POST'])
def newData():
    # try:
    bids = bid.query.all()
    json_data = request.json['info']
    rooms = len(json_data['bid_tables'])
    print(json_data['info'])
    bid_arr = []
    roommates =[]
    total_rent =0
    for i in range(0,rooms):
        b = [json_data['bid_tables'][i]['room'],json_data['bid_tables'][i]['roommate'],json_data['bid_tables'][i]['rent']]
        bid_arr.append(b)
        roommates.append(json_data['bid_tables'][i]['roommate'])
        total_rent += int(json_data['bid_tables'][i]['rent'])
   
    rp = roompicker.RoomPicker(roommates=roommates, total_rent=int(total_rent),old = True,old_list=bid_arr,turn = json_data['turn'])
    rp.run_algo(in_room_number=int(json_data['info']['bid_name']), in_bid=int(json_data['info']['total'])) 
    info = json.loads(rp.rooms_df.to_json())
    rooms = len(info['roommate'])+1
    dataList = []
    for i in range(1,rooms):
        dataDetail = {
            'room':i,
            'roommate':info['roommate'][str(i)],
            'rent':info['rent'][str(i)],
        }
        dataList.append(dataDetail)

    dataUpload={'bidder_name':rp.roommates[rp.turn],'turn': json_data['turn'],'rooms':dataList}

    return json.dumps(dataUpload)
    # except Exception as e:
    #     return str(e)

@app.route('/passData',methods=['POST'])
def passData():
    # try:
    json_data = None
    bids = bid.query.all()
    json_data = request.json['info']
    rooms = len(json_data['bid_tables'])
    print(json_data['info'])
    bid_arr = []
    roommates =[]
    total_rent =0
    for i in range(0,rooms):
        b = [json_data['bid_tables'][i]['room'],json_data['bid_tables'][i]['roommate'],json_data['bid_tables'][i]['rent']]
        bid_arr.append(b)
        roommates.append(json_data['bid_tables'][i]['roommate'])
        total_rent += int(json_data['bid_tables'][i]['rent'])
   
    rp = roompicker.RoomPicker(roommates=roommates, total_rent=int(total_rent),old = True,old_list=bid_arr,turn = json_data['turn'])
    rp.pass_dude()
    info = json.loads(rp.rooms_df.to_json())
    rooms = len(info['roommate'])+1
    dataList = []
    for i in range  (1,rooms):
        dataDetail = {
            'room':i,
            'roommate':info['roommate'][str(i)],
            'rent':info['rent'][str(i)],
        }
        dataList.append(dataDetail)
    dataUpload = None
    dataUpload={'bidder_name':rp.roommates[rp.turn],'turn': rp.turn,'rooms':dataList}

    return json.dumps(dataUpload)
    # except Exception as e:
    #     return str(e)

@app.route('/getData',methods=['POST'])
def getData():
    # try:
    bids = bid.query.all()
    json_data = request.json['info']
    # dataRow = bids.query.filter(id=dataID)
    rp = roompicker.RoomPicker(roommates=json_data['members'], total_rent=json_data['total'],old = False,old_list=[],turn = 0)
    info = json.loads(rp.rooms_df.to_json())
    rooms = len(info['roommate'])+1
    dataList = []
    roommates = []
    for i in range(1,rooms):
        dataDetail = {
            'room':i,
            'roommate':info['roommate'][str(i)],
            'rent':info['rent'][str(i)],
        }
        
        dataList.append(dataDetail)

    dataUpload={'bidder_name':rp.roommates[rp.turn],'turn': rp.turn,'rooms':dataList}

    return json.dumps(dataUpload)
    # except Exception as e:
    #     return str(e)

@app.route("/addData",methods=['POST'])
def addData():
    # try:
    json_data = request.json['info']
    bid_name = json_data['bid_name']
    total = json_data['total']
    ms = json_data['members']
    mr = ms.split(',')

    taco = bid(bid_name, total)
    db.session.add(taco)
    db.session.commit()
    for m in mr:
        burrito = member(m,taco)
        db.session.add(burrito)
        db.session.commit()

    for t in members:
        print(t)


    return jsonify(status='OK',message='inserted successfully')

    # except Exception as e:
    #     return jsonify(status='ERROR',message=str(e))
