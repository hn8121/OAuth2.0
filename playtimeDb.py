#!usr/bin/env python3
"""Playground for testing SQL."""
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem, User


engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# inspector allows you to inspect the database
# inner "for" will show all columns for each table
inspector = inspect(engine)
for table_name in inspector.get_table_names():
   print("**** Table: %s" % table_name)
   for column in inspector.get_columns(table_name):
       print("Column: %s" % column['name'])

table_name = 'restaurant'
#table_name = 'user'
#select the contents of each table
selstmt = """SELECT * FROM """ + table_name
print(selstmt)
resultset = session.execute(selstmt).fetchall()
for i in resultset:
    print(i)

#delete example
#delset = session.query(Restaurant).filter_by(id > 9)
#session.delete(delset)
#session.commit()

#selstmt = """SELECT restaurant_id, count(*) as numItems FROM menu_item GROUP BY restaurant_id"""
#print(selstmt)
#resultset = session.execute(selstmt).fetchall()

#for i in resultset:
#    print("id %s: %s" % (i.restaurant_id, i.numItems))




selstmt = """SELECT * FROM menu_item"""
#resultset = session.execute(selstmt).fetchall()
#for item in resultset:
#    print ("%s - %s - %s - %s - %s" % (item.id, item.name, item.description, item.price, item.course))

selstmt = """SELECT distinct(course) FROM menu_item where restaurant_id = '8'""" 
selstmt = """SELECT restaurant_id FROM menu_item where restaurant_id = '8'""" 
#resultset = session.execute(selstmt).fetchall()
#print("%s" % str(resultset))

selstmt = """SELECT id, name, description, price, course, restaurant_id FROM menu_item WHERE restaurant_id=1"""
selstmt = selstmt + """ ORDER BY 1 """   
#print(selstmt)
#resultset = session.execute(selstmt).fetchall()
#for i in resultset:
    #print(i)

#items = session.query(MenuItem).all()
#print(items[0].name)

### use filterby to isolate a specific column in the table.
#veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
#for vburger in veggieBurgers:
#    print(vburger.id, vburger.price, vburger.restaurant.name)

# get only 1st veggie burger item from urban veggie burger restaurant
# id value found from previous query.
#urbanVeggieBurger = session.query(MenuItem).filter_by(id = 1).one()
#print(urbanVeggieBurger.price)
#urbanVeggieBurger.price = '$7.50'
#session.add(urbanVeggieBurger)
#session.commit()

#for vburger in veggieBurgers:
#    print(vburger.id, vburger.price, vburger.restaurant.name)

#delete example
#spinach = session.query(Restaurant).filter_by(id = '18').one()
#print(spinach.name)
#session.delete(spinach)
#session.commit()
#print(spinach)

#rname = webserver_sql.get_restaurant_name_from_id(12)
#rname = session.query(Restaurant).filter_by(id=12).one()
#print(rname.name)
