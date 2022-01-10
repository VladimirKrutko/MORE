import psycopg2
import smtplib
class More_DB_commnad:
    
    def __init__(self, db_name, username, password, host='localhost'):
        self.connect = psycopg2.connect(dbname=db_name, user=username, 
                        password=password, host=host)
        self.smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        self.smtpObj.starttls()

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
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            query = f'INSERT INTO more_table.saplier (name, email, tel) VALUES (\'{sap_name}\', \'{email}\',\'{tel}\');'
            cursor.execute(query)
    
    def insert_delivery_warehouse (self, prod_name, c_name, sup_name,u_price, quant):
        with self.conect.cursor() as cursor:
            self.connect.autocommit = True
            query = f'SELECT  more_table.insert_deliver_warehouse(\'{prod_name}\'::text,\'{c_name}\'::text, \'{sup_name}\'::text, {u_price}::float, {quant}::float);'
            cursor.execute(query)

    def select_country(self):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            cursor.execute('SELECT * FROM more_table.country;')
            country = [{'id':row[0], 'country':row[1]} for row in cursor.fetchall()]
        return country 
    
    def select_suplier(self):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            cursor.execute('SELECT * FROM more_table.saplier;')
            sapplier = [{'id': row[0], 'name':row[1], 'email':row[2], 'tel':row[3]}  
                        for row in cursor.fetchall()]
        return sapplier
    
    def select_delivery(self):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            cursor.execute('SELECT p.name product, c.name country, s.name sapplier,d.unit_price, d.quantity,d.date date '+
            'FROM more_table.delivery d '+
            'JOIN more_table.product p ON p.idproduct = d.idproduct '+
            'JOIN more_table.country c  ON d.idcountry = c.idcountry '+
            'JOIN more_table.saplier s ON s.idsaplier = d.idsumplier;')
            delivery = [{ name:obj for name,  obj in  zip(['product', 'country', 'sapplier','unit_price', 'quantity', 'date'] ,row)} for row in cursor.fetchall()]
        return delivery
    
    def select_warehouse(self):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            cursor.execute('SELECT w.idstatemant, p.name product, w.quantity, w.date last_update '+
                        'FROM more_table.warehouse w '+
                        'JOIN product p ON p.idproduct = w.idproduct;')
            status = [{name: obj for name, obj in zip(['idstatemant','product', 'quantity','last_update'] ,row)}
                    for row in cursor.fetchall()]
        return status

    def insert_sales(self, name_product, quantity):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            query = f"SELECT more_table.sales_(\'{name_product}\'::text, {quantity});"
            cursor.execute(query)
        return 0
    
    def send_email(self, sap_email, prod_name):
        with self.connect.cursor() as cursor:
            self.connect.autocommit = True
            query = ("SELECT p.name, w.quantity "
            +" FROM more_table.warehouse w"
            +" JOIN more_table.product p ON w.idproduct=p.idproduct" 
            +f" WHERE p.name =\'{prod_name}\';")
            cursor.execute(query)
            status =  cursor.fetchall()
        if status[0][1]<=0:
            self.smtpObj.login('krutkovova09gmail.com@mail.ru','Ea1adeMPpALyk4PqcXwt')
            # self.smtpObj.sendmail('krutkovova09gmail.com@mail.ru', 'krutkovova24@gmail.com', 
            # u''.join(prod_name).encode('utf-8')+'-20'.encode('utf-8'))
            print ('Sended email ot sapplier')


    