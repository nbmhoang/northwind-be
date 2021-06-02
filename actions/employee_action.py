import sqlite3

from ..models import employee_model

class EmployeeAction:

    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def get_all(self):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = 'SELECT * FROM tbl_employee'
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            emp = employee_model.Employee(
                employee_id=row[0],
                last_name=row[1],
                first_name=row[2],
                birth_date=row[3],
                photo=row[4],
                notes=row[5]
            )
            result.append(emp.serialize())
        return result



    def get_by_id(self, id):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            SELECT * FROM tbl_employee WHERE employee_id = ?
        """
        # (id,)
        cursor.execute(sql, (id, ))
        row = cursor.fetchone()
        if row == None:
            return 'Employee not found', 404
        emp = employee_model.Employee(
                employee_id=row[0],
                last_name=row[1],
                first_name=row[2],
                birth_date=row[3],
                photo=row[4],
                notes=row[5]
            )
        return emp, 200

    def add(self, employee: employee_model.Employee):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_employee
            VALUES(null, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (employee.last_name, employee.first_name, employee.birth_date, employee.photo, employee.notes))
        conn.commit()
        return 'Inserted successfully!'
    
    def delete(self, employee: employee_model.Employee):
        """
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            # DELETE FROM tbl_customer WHERE customer_id = ?
        """
        cursor.execute(sql, (customer.customer_id,))
        conn.commit()
        count = cursor.rowcount
        if count == 0:
            return 'Customer not found', 404
        return 'Deleted successfully', 200
        """

    def update(self, id: int, employee: employee_model.Employee):
        """
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            # UPDATE tbl_customer
            # SET customer_name = ?, contact_name = ?, address = ?, city = ?, postal_code = ?, country = ?
            # WHERE customer_id = ?
        """
        cursor.execute(sql, (customer.customer_name, customer.contact_name, customer.address, customer.city, customer.postal_code, customer.country, id))
        conn.commit()
        n = cursor.rowcount
        if n == 0:
            return 'Customer not found', 404
        return 'Updated successfully', 200
        """