# Connect to DB
# Query and return result
import sqlite3

from ..models import customer_model

class CustomerAction:

    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def get_all(self):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = 'SELECT * FROM tbl_customer'
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            customer = customer_model.Customer(
                customer_id=row[0],
                customer_name=row[1],
                contact_name=row[2],
                address=row[3],
                city=row[4],
                postal_code=row[5],
                country=row[6]
            )
            result.append(customer.serialize())
        return result



    def get_by_id(self, id):
        pass

    def add(self, customer: customer_model.Customer):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            INSERT INTO tbl_customer
            VALUES(null, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (customer.customer_name, customer.contact_name, customer.address, customer.city, customer.postal_code, customer.country))
        conn.commit()
        return 'Inserted successfully!'
    
    def delete(self, customer: customer_model.Customer):
        pass

    def update(self, id, customer: customer_model.Customer):
        pass