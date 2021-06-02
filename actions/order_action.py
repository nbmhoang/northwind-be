import sqlite3

from ..models import customer_model, order_model, shipper_model, employee_model

class OrderAction:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_all(self):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
        SELECT tbl_order.order_id, tbl_order.order_date, customer.customer_id, customer.customer_name, customer.contact_name, customer.address, customer.city, customer.postal_code, customer.country,
                employee.employee_id, employee.first_name, employee.last_name, employee.birth_date, employee.photo, employee.notes,
                shipper.shipper_id, shipper.shipper_name, shipper.phone
        FROM tbl_order 
        JOIN tbl_customer customer
        ON tbl_order.customer_id == customer.customer_id
        JOIN tbl_employee employee
        ON tbl_order.employee_id == employee.employee_id
        JOIN tbl_shipper shipper
        ON tbl_order.shipper_id == shipper.shipper_id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            customer = customer_model.Customer(
                customer_id=row[2],
                customer_name=row[3],
                contact_name=row[4],
                address=row[5],
                city=row[6],
                postal_code=row[7],
                country=row[8]
            )
            employee = employee_model.Employee(
                employee_id=row[9],
                first_name=row[10],
                last_name=row[11],
                birth_date=row[12],
                photo=row[13],
                notes=row[14]
            )
            shipper = shipper_model.Shipper(
                shipper_id=row[15],
                shipper_name=row[16],
                phone=row[17]
            )
            order = order_model.Order(
                order_id=row[0],
                order_date=row[1],
                customer=customer,
                employee=employee,
                shipper=shipper
            )
            result.append(order.serialize())
        return result


    def get_by_id(self, id):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
        SELECT tbl_order.order_id, tbl_order.order_date, customer.customer_id, customer.customer_name, customer.contact_name, customer.address, customer.city, customer.postal_code, customer.country,
                employee.employee_id, employee.first_name, employee.last_name, employee.birth_date, employee.photo, employee.notes,
                shipper.shipper_id, shipper.shipper_name, shipper.phone
        FROM tbl_order 
        JOIN tbl_customer customer
        ON tbl_order.customer_id == customer.customer_id
        JOIN tbl_employee employee
        ON tbl_order.employee_id == employee.employee_id
        JOIN tbl_shipper shipper
        ON tbl_order.shipper_id == shipper.shipper_id
        WHERE tbl_order.order_id = ?
        """
        cursor.execute(sql, (id, ))
        row = cursor.fetchone()
        if row == None:
            return 'Order not found', 404
        customer = customer_model.Customer(
            customer_id=row[2],
            customer_name=row[3],
            contact_name=row[4],
            address=row[5],
            city=row[6],
            postal_code=row[7],
            country=row[8]
        )
        employee = employee_model.Employee(
            employee_id=row[9],
            first_name=row[10],
            last_name=row[11],
            birth_date=row[12],
            photo=row[13],
            notes=row[14]
        )
        shipper = shipper_model.Shipper(
            shipper_id=row[15],
            shipper_name=row[16],
            phone=row[17]
        )
        order = order_model.Order(
            order_id=row[0],
            order_date=row[1],
            customer=customer,
            employee=employee,
            shipper=shipper
        )
        return order, 200

    def add(self, order: order_model.Order):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_order
            VALUES(null, ?, ?, ?, ?)
        """
        cursor.execute(sql, (order.customer.customer_id, order.employee.employee_id, order.order_date, order.shipper.shipper_id))
        conn.commit()
        return 'Inserted successfully!'

    def update(self, id, order):
        pass

    def delete(self, order):
        pass