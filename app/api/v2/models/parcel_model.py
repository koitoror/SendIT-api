import psycopg2
import psycopg2.extras
from flask_jwt_extended import get_jwt_identity

url = "dbname='SendIT' host='localhost' port='5432' user='postgres' password='new1'"

class Parcels():
   def __init__(self, user_id=None, sender_name=None, phone_number=None, id_number=None, location=None, address=None, weight=None, destination=None, price =None):
       self.user_id = user_id
       self.sender_name = sender_name
       self.phone_number = phone_number
       self.id_number = id_number
       self.location = location
       self.address = address
       self.weight = weight
       self.destination = destination
       self.price = 10

   def store_in_db(self):
       #save parcel order in database
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       print(self.price)
       query = "insert into orders VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       cur.execute(query, (self.user_id,self.sender_name, self.phone_number, self.id_number,
                           self.location, self.address, self.weight,
                           self.destination, self.price))
       con.commit()
       con.close()

   def get_all_parcels(self):
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = "SELECT * FROM orders ;"
       cur.execute(query)
       parcels = cur.fetchall()
       result = [] #to append json object created
       for parcel in parcels:
           object = {
               "order_id":parcel["order_id"],
               "sender_name": parcel["sender_name"],
               "phonenumber": parcel["phone_number"],
               "idnumber": parcel["id_number"],
               "location": parcel["location"],
               "address": parcel["address"],
               "weight": parcel["weight"],
               "destination": parcel["destination"],
               "price": parcel["price"],
               "status": parcel["status"],
           }
           result.append(object)
       return result

   def get_parcel_by_id(self, order_id):
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = "SELECT * FROM orders WHERE order_id=%s"
       parcels=cur.execute(query,(order_id,))
       parcels = cur.fetchall()
       result = []
       print(parcels)
       for parcel in parcels:
           object = {
           "order_id": parcel[0],
           "user_id": parcel[1],
           "sender_name": parcel[2],
           "phonenumber": parcel[3],
           "idnumber": parcel[4],
           "location": parcel[5],
           "address": parcel[6],
           "weight": parcel[7],
           "destination": parcel[8],
           "price": parcel[9],
           "status": parcel[10],
           }
           result.append(object)
       return result

   def cancel_order(self, order_id):
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = "SELECT * FROM orders WHERE order_id='{}';".format(order_id)
       cur.execute(query)
       orders = cur.fetchone()
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = "UPDATE orders set status='cancelled' WHERE order_id='{}';".format(order_id)
       cur.execute(query)
       con.commit()


   def specific_user_order(self, user_id):
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = "SELECT * FROM orders WHERE user_id='{}';".format(user_id)
       cur.execute(query, (user_id,))
       row = cur.fetchall()
       order = row
       return order

   def change_destination(self, destination, order_id):
       con = psycopg2.connect(url)
       cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = "SELECT * FROM orders WHERE order_id='{}';".format(order_id)
       cur.execute(query)
       response = cur.fetchone()
       if not response:
           return False
       query = "UPDATE orders SET destination='{}' WHERE order_id={}".format(destination, order_id)
       response = cur.execute(query)
       con.commit()
       return True









