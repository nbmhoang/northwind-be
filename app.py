from flask import Flask, json
from flask import jsonify

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
    pass

@app.route('/customer', methods=['POST'])
def add_customer():
    pass