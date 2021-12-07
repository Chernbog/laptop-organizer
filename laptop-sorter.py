# Regular Utilities

import uuid # https://docs.python.org/3/library/uuid.html#uuid.uuid4 - Generate random uuid for laptop
import sys # https://docs.python.org/3/library/sys.html#sys.exit - exit the program

# Database Utilities

import csv

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


# Configuration

create_sqlite_database = False # Set to True to create the database

# once the database file is created this should be set to False
# so no other duplicates arise.

start_data_entry = False # Set to True to start data entry process

show_data = False # Set to True to see all database information

show_sqlite_debug = False # Set to True to see sqlite debug

convert_to_csv = False # Set to True to convert the database to a csv file (Make sure to set everything else false)

# Make user be able to customize csv name and db name

# SQLITE DATABASE

# (Optional) Set the name of the database here ex. 'sqlite:///my-laptop-database.db'
engine = create_engine('sqlite:///laptop-v5.db', echo = show_sqlite_debug)


Base = declarative_base()


class laptops(Base):

    __tablename__ = 'laptops'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    condition = Column(String)
    model = Column(String)


if create_sqlite_database == True:
    Base.metadata.create_all(engine)
else:
    print('[ OK ] Laptop database running...')

def database_input_data(laptop_data):
    with Session(engine) as session:
        session.add(laptop_data)
        session.commit()

def database_show_data():
    with Session(engine) as session:
        data = session.query(laptops).all()
        for row in data:
            a = (f'uuid: {row.uuid} condition: {row.condition}  model: {row.model}')

            print(type(a))
            print(a)

def database_to_csv():
    with Session(engine) as session:

        data = session.query(laptops).all()

        print('[ OK ] Converting database to csv...')

        with open('laptop-v3.csv', 'w', newline='') as csvfile:
            fieldnames = ['uuid', 'condition', 'model']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for laptop in data:
                a = laptop.uuid
                b = laptop.condition
                c = laptop.model

                writer.writerow({'uuid': a, 'condition': b, 'model': c})

# DATA ENTRY

def laptop_data():

    # LAPTOP CONDITION
    
    laptop_condition_input = input('\nEnter Laptop condition \n 1. Good - Ready to Provision \n 2. Good Minor Damage - Ready to Provision \n 3. Bad - Needed for disposal \n 4.Exit \n Enter number: ')

    laptop_condition_number = int(laptop_condition_input)

    laptop_condition = []

    if laptop_condition_number == 1:
        laptop_condition.append('Good Quality - Ready To Provision')
    if laptop_condition_number == 2:
        laptop_condition.append('Medium Quality - Ready To Provision')
    if laptop_condition_number == 3:
        laptop_condition.append('Bad Quality - Do Not Provision')
    if laptop_condition_number == 4:
        sys.exit()

    laptop_condition_type = laptop_condition[0]

    # LAPTOP MODEL NAME

    laptop_model_input = input('Enter Laptop Model \n 1. x140e \n 4. Exit \n Enter Number: ')

    laptop_model_number = int(laptop_model_input)

    laptop_model = []

    if laptop_model_number == 1:
        laptop_model.append('x140e')
    if laptop_condition_number == 4:
        sys.exit()
    
    if show_sqlite_debug == True:
        print('\nDEBUG INFORMATION:\n')
    else:
        pass
    
    laptop_model_type = laptop_model[0]

    laptop_uuid = uuid.uuid4()

    laptop_uuid_str = str(laptop_uuid)

    laptop_metadata = dict(UUID=laptop_uuid_str, Condition=laptop_condition_type, Model=laptop_model_type)

    return(laptop_metadata)

def data_entry():
    laptop_info = laptop_data()

    laptop_final = laptops(uuid = laptop_info['UUID'], condition = laptop_info['Condition'], model = laptop_info['Model'])

    database_input_data(laptop_final)

    if show_data == True:
        database_show_data()
    else:
        pass


if start_data_entry == True:
    while start_data_entry == True:
        data_entry()
else:
    pass

if convert_to_csv == True:
    database_to_csv()
else:
    pass