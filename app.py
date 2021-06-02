from flask import Flask, json
from flask import jsonify
from flask import request
from time import time

from flask import send_file

from .actions.customer_action import CustomerAction
from .models.customer_model import Customer
from .actions.order_action import OrderAction
from .actions.employee_action import EmployeeAction
from .models.order_model import Order
from .models.employee_model import Employee
from .models.shipper_model import Shipper
from .models import employee_model


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

@app.route('/orders')
def get_all_order():
    order_action = OrderAction(connection_data)
    orders = order_action.get_all()
    return jsonify(orders)

@app.route('/order/<int:id>')
def get_order_by_id(id):
    order_action = OrderAction(connection_data)
    result, status_code = order_action.get_by_id(id)
    if status_code == 200:
        return jsonify(result.serialize()), status_code
    return jsonify({
        'message': result
    }), status_code

@app.route('/order', methods=['POST'])
def add_order():
    # form_data = request.form
    data = request.json

    customer_id = data.get('customer_id', 0)
    employee_id = data.get('employee_id', 0)
    shipper_id = data.get('shipper_id', 0)
    order_date = data.get('order_date', '')

    customer = Customer(customer_id=customer_id)
    employee = Employee(employee_id=employee_id)
    shipper = Shipper(shipper_id=shipper_id)

    order = Order(customer=customer, employee=employee,  order_date=order_date, shipper=shipper)

    action = OrderAction(connection_data)
    message = action.add(order)
    return jsonify({
        'message': message
    })

# Write API for Order

@app.route('/employees')
def get_all_employee():
    action = EmployeeAction(connection_data)
    employees = action.get_all()
    return jsonify(employees)


@app.route('/employee', methods=['POST'])
def add_employee():
    form_data = request.form

    birth_date = form_data.get('birth_date', '01/01/2000')
    first_name = form_data.get('first_name', '')
    last_name = form_data.get('last_name', '')
    notes = form_data.get('notes', '')
    # Timestamp
    # UUID
    photo = request.files['photo']

    filename = str(int(time())) + '.jpg'
    photo.save(f'uploads/{filename}')

    employee = employee_model.Employee(
        last_name=last_name,
        first_name=first_name,
        birth_date=birth_date,
        notes=notes,
        photo=filename
    )

    action = EmployeeAction(connection_data)
    result = action.add(employee)
    return jsonify({
        'message': result
    })

@app.route('/images/<string:image_name>')
def get_images(image_name):
    return send_file(f'uploads/{image_name}', mimetype='image/jpeg')