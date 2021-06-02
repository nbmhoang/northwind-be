from flask import Flask, json
from flask import jsonify
from flask import request

from .actions.customer_action import CustomerAction
from .models.customer_model import Customer 


app = Flask(__name__)

connection_data = './db.sqlite3'

"""
METHOD:
    1. GET
    2. POST
    3. PUT(PATCH)
    4. DELETE
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = {
        'message': 'Hello World',
        'status': 'Success'
    }
    return jsonify(result)

@app.route('/index', methods=['POST'])
def index():
    return 'Index page'

# Get all customer
@app.route('/customers')
def get_customer():
    customer_action = CustomerAction(connection_data)
    result = customer_action.get_all()
    return jsonify(result)

@app.route('/customer/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_or_modify_customer(id):
    if request.method == 'GET':
        # Get customer by id
        customer_action = CustomerAction(connection_data)
        result, status_code = customer_action.get_by_id(id)
        if status_code == 200:
            return jsonify(result.serialize()), status_code
        return jsonify({
            'message': result
        }), status_code
    elif request.method == 'PUT':
        # Update customer by id
        body = request.json # dictionary

        customer_name = body.get('customer_name', '')
        contact_name = body.get('contact_name', '')
        addresss = body.get('address', '')
        city = body.get('city', '')
        postal_code = body.get('postal_code', '')
        country = body.get('country', '')

        customer = Customer(customer_name=customer_name, contact_name=contact_name, \
        address=addresss, city=city, postal_code=postal_code, country=country)
        
        customer_action = CustomerAction(connection_data)
        message, status_code = customer_action.update(id, customer)
        return jsonify({
            'message': message
        }), status_code
    elif request.method == 'DELETE':
        # Delete customer by id
        customer = Customer(customer_id=id)
        customer_action = CustomerAction(connection_data)
        message, status_code = customer_action.delete(customer)
        return jsonify({
            'message': message
        }), status_code
    else:
        # 405
        pass

@app.route('/customer', methods=['POST'])
def add_customer():
    # Get data from request body
    body = request.json # dictionary

    customer_name = body.get('customer_name', '')
    contact_name = body.get('contact_name', '')
    addresss = body.get('address', '')
    city = body.get('city', '')
    postal_code = body.get('postal_code', '')
    country = body.get('country', '')

    customer = Customer(customer_name=customer_name, contact_name=contact_name, \
        address=addresss, city=city, postal_code=postal_code, country=country)
    customer_action = CustomerAction(connection_data)
    result = customer_action.add(customer)
    return jsonify({
        'message': result
    }), 201