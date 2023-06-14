#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response


#DELIVERABLE 1:
#Define a POST block inside of a /baked_goods route
#creates a new baked good in the database and 
#returns its data as JSON. The request will send data in a form.
#add method = ['POST'] bd GET is the defualt
@app.route('/baked_goods', methods=['POST', 'GET'])
def baked_goods():
    baked_goods = BakedGood.query.all()
    if request.method == 'GET':
        bg_serialized = [bg.to_dict() for bg in baked_goods]


        response = make_response(
            jsonify(bg_serialized),
            200
        )

        return response
    elif request.method == 'POST':
        #THIS IS AN INSTANCE OF THE CLASS BAKEDBOOD
        new_baked_good = BakedGood(
            name=request.form.get('name'),
            price=request.form.get('price'),
            bakery_id=request.form.get('bakery_id'),
        )

        db.session.add(new_baked_good)
        db.session.commit()

        new_baked_good_dict = new_baked_good.to_dict()

        response = make_response(
            jsonify(new_baked_good_dict),
            201
        )

        return response


#DELIVERABLE 2
#Define a PATCH block inside of the /bakeries/<int:id> route 
#that updates the name of the bakery in the database 
#and returns its data as JSON. As with the previous POST block, 
#the request will send data in a form. 
#The form does not need to include values 
#for all of the bakery's attributes.
@app.route('/bakeries/<int:id>', methods=['PATCH', 'GET'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    elif request.method == 'PATCH':
        #for each attribute you want to change in the request.form
        #setattr() param1=query variable, param2=attribute to be changed
        #param3=request.form.get(attribute)
        #for attr in request.form:
                #setattr(review, attr, request.form.get(attr))
        for name in request.form:
                setattr(bakery, name, request.form.get(name))
        db.session.add(bakery)
        db.session.commit()

        #TURN SQL/PYTHON CODE TO JSON CODE
        bakery_dict = bakery.to_dict()

        response = make_response(
            jsonify(bakery_dict),
            200
        )

        return response


#DELIVERABLE 3
#Define a DELETE block inside of a /baked_goods/<int:id> route 
#that deletes the baked good from the database and 
#returns a JSON message 
#confirming that the record was successfully deleted.
@app.route('/baked_goods/<int:id>', methods= ['DELETE', 'GET'])
def delete_goods(id):
    #you are getting ONE ITEM, so name is SINGULAR
    good = BakedGood.query.filter(BakedGood.id == id).first()
    if request.method == 'GET':
        #DONT need a list so leave it OUT of brackets
        #the query variable is ONE ITEM, so you only need the ONE
        #item to turn into a dictionary
        goods_serialized = good.to_dict()

        response = make_response(
            jsonify(goods_serialized),
            200
        )
        return response
    
    elif request.method == 'DELETE':
        #use the delete method on the thing you want to be deleted
        #in this case, we did a query to access ONE good
        #pass that variable...good...as the argument
        db.session.delete(good)
        db.session.commit()

        #need to send a response back to say that it was successful
        response_body = {
                "delete_successful": True,
                "message": "Review deleted."    
            }

        response = make_response(
            jsonify(response_body),
            200
        )

        return response





@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
