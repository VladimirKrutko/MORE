import psycopg2

class Insert_data:
    
    def __init__(self, db_name, username, password, host='localhost'):
        conect = psycopg2.connect(dbname=db_name, user=username, 
                        password=password, host=host)


    def insert_product(self, prod_name, unit):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            query = f'INSERT INTO more_table.product (name, unit) VALUES (\'{prod_name}\', \'{unit}\');'
            cursor.execute(query)
    
    def insert_country(self, country):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            query = f'INSERT INTO more_table.country (name) VALUES (\'{country}\');'
            cursor.execute(query)

    def insert_sapplier(self, sap_name, email, tel):
        with self.conect.cursor() as cursor:
            self.connect.autocommit = True
            query = f'INSERT INTO more_table.saplier (name, email, tel) VALUES (\'{sap_name}\', \'{email}\',\'{tel}\');'
            cursor.execute(query)
    
    def insert_delivery_warehouse (self, prod_name, c_name, sup_name,u_price, quant):
        with self.conect.cursor() as cursor:
            self.connect.autocommit = True
            query = f'SELECT  more_table.insert_deliver_warehouse(\'{prod_name}\'::text,\'{c_name}\'::text, \'{sup_name}\'::text, {u_price}::float, {quant}::float);'
            cursor.execute(query)
    
