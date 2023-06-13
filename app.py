from flask import Flask, request, jsonify, render_template
from pony.orm import Database, Required, Optional, PrimaryKey, db_session, select, desc
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Goods(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    quantity = Required(int)
    type = Required(str)
    entry_date = Required(datetime)
    exit_date = Optional(datetime)

db.generate_mapping(create_tables=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/goods', methods=['POST'])
@db_session
def add_goods():
    data = request.get_json()
    good = Goods(
        name=data['name'],
        quantity=int(data['quantity']),  
        type=data['type'],
        entry_date=datetime.strptime(data['entry_date'], '%Y-%m-%d'),
        exit_date=datetime.strptime(data['exit_date'], '%Y-%m-%d') if data.get('exit_date') else None
    )
    db.commit()
    return jsonify(success=True, id=good.id)

@app.route('/goods/<int:good_id>', methods=['GET'])
@db_session
def get_good(good_id):
    good = Goods.get(id=good_id)
    if good is None:
        return {"error": "Good not found"}, 404
    return jsonify(
        id=good.id,
        name=good.name,
        quantity=good.quantity,
        type=good.type,
        entry_date=good.entry_date.strftime('%Y-%m-%d'),
        exit_date=good.exit_date.strftime('%Y-%m-%d') if good.exit_date else None
    )

@app.route('/goods/<int:good_id>', methods=['PUT'])
@db_session
def update_good(good_id):
    good = Goods.get(id=good_id)
    if good is None:
        return {"error": "Good not found"}, 404
    data = request.get_json()
    good.name = data.get('name', good.name)
    good.quantity = int(data.get('quantity', good.quantity))  
    good.type = data.get('type', good.type)
    good.entry_date = datetime.strptime(data.get('entry_date', good.entry_date.strftime('%Y-%m-%d')), '%Y-%m-%d')
    good.exit_date = datetime.strptime(data.get('exit_date', good.exit_date.strftime('%Y-%m-%d') if good.exit_date else None), '%Y-%m-%d') if data.get('exit_date') else None
    db.commit()
    return jsonify(success=True)

@app.route('/goods/<int:good_id>', methods=['DELETE'])
@db_session
def delete_good(good_id):
    good = Goods.get(id=good_id)
    if good is None:
        return {"error": "Good not found"}, 404
    good.delete()
    db.commit()
    return jsonify(success=True)

@app.route('/goods', methods=['GET'])
@db_session
def get_goods():
    goods_type = request.args.get('type')
    sort = request.args.get('sort')

    if goods_type and sort:
        if sort == 'desc':
            goods = select(g for g in Goods if g.type == goods_type).order_by(lambda g: desc(g.entry_date))[:]
        else:
            goods = select(g for g in Goods if g.type == goods_type).order_by(Goods.entry_date)[:]
    else:
        if goods_type:
            goods = select(g for g in Goods if g.type == goods_type)[:]
        elif sort:
            if sort == 'desc':
                goods = select(g for g in Goods).order_by(lambda g: desc(g.entry_date))[:]
            else:
                goods = select(g for g in Goods).order_by(Goods.entry_date)[:]
        else:
            goods = select(g for g in Goods)[:]

    goods_list = [g.to_dict() for g in goods]
    return jsonify(goods_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)