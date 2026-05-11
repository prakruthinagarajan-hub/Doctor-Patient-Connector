import sys
import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',password='manager',database='medical_store')
c1=conn.cursor()
from time import gmtime, strftime
a=strftime("%a ,%d %b %y %H:%M:%S",gmtime())
if conn.is_connected:
    print("                                                       CONNECTOR             ")
    print(a)
    print("1. Login")
    print("2. Exit")
    print()
    option=int(input("Enter your choise : "))
    if option==1:
        print()
        user=input('User Name : ')
        user=user.upper()
        c1.execute("select * from account_details where User_Name like '" + user + "'")
        datas=c1.fetchall()
        for i in datas:
            value_1=i[0]
            value_2=i[1]
        if user==value_1:
            password=input('Password : ')
            password=password.upper()
            if password==value_2:
                print()
                print('Login successfull')
                print()
                print("11.Customers Account")
                print("12.Medicine Cost")
                print("3.Bill")
                print()
                option=int(input("enter a option:"))
                if option==11:
                                account_number=int(input("enter your acct_number:"))
                                patient_name=input("enter your name:")
                                age=int(input("enter your age:"))
                                address=input("enter your address:")
                                phone_number=int(input("enter your number:"))
                                balance_amount=float(input("enter your amount:"))
                                x="insert into customers_details values("+str(account_number)+",'"+patient_name+"',"+str(age)+",'"+address+"',"+str(phone_number)+","+str(balance_amount)+")"
                                print(x)
                                c1.execute(x)
                                print("Account created congrats")
                                conn.commit()
                if option==12:
                    print("records created")
                if option==3:
                    print(a)
                    patient_name=input("enter the patient_name :")
                    no=int(input('enter the number of medicine:'))
                    print('customer name:',patient_name)
                    for i in range (no):
                        med_name=input('enter medicine name : ')
                        c1.execute("select medicine_code,gst,sgst,total_cost from medicines_details where medicine_name like '" + str(med_name) +"'" )
                        data=c1.fetchall()
                        for row in data:
                            print('medicine_code of',med_name,':',row[0])
                            print('gst of',med_name,':',row[1])
                            print('sgst of',med_name,':',row[2])
                            print('cost_per_item of',med_name,':',row[3])
                            conn.commit()
                            account_number=input('enter account_number:')
                            c1.execute("select balance_amount from customers_details where account_number like'"+str(account_number)+"'")
                            datas=c1.fetchall()
                            datas=list(datas[0])
                            datas=datas[0]
                            print(datas)
                            conn.commit()
                            print("rows affected:",c1.rowcount)
                            conn.commit()
                            quantity=int(input("enter the quantity:"))
                            total_amount=row[3]*quantity
                            print("total_amount of",med_name,':',total_amount)
                            v_sql_insert="insert into SS_bill (medicine_name,medicine_code,gst,sgst,cost_per_item,quantity,discount_on_balance_amount,total_amount)values('{}',{},{},{},{},{},{},{})".format(med_name,row[0],row[1],row[2],row[3],quantity,datas,total_amount)
                            print(v_sql_insert)
                            c1.execute(v_sql_insert)
                            conn.commit()
                            print("Records added")
             
            else:
                print('Invalid Password')
                print('Tryagain')
    elif option==2:
        print("              THANK YOU VISIT AGAIN                  ")
        sys.exit()
    
                    
                    
                
                
                
                         
                               


                
                
                           

                           

                
                                   
                
           
