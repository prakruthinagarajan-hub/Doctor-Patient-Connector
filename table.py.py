import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',password='manager',database='medical_store')
if conn.is_connected:
                print('successfully connected')
c1=conn.cursor()
c1.execute('create table account_details(User_Name varchar(30)primary key,password varchar(30) unique)')
c1.execute('create table customers_details(account_number int primary key,patient_name varchar(30),age int,address varchar(50),phone_number bigint(11),balance_amount float)')
c1.execute('create table medicines_details(medicine_name varchar(30),medicine_code int,gst float,sgst float,total_cost float)')
c1.execute('create table SS_bill(medicine_name varchar(30),medicine_code int ,gst float,sgst float,cost_per_item float,quantity int,discount_on_balance_amount float,total_amount float)')
print('table created')
