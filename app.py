#import pandas as pd
from pymongo import MongoClient
import streamlit as st
import db

#---------------MONGODB CONNECTION---------------
@st.experimental_singleton
def init_connection():
    return MongoClient("mongodb+srv://oscarmejias:oscar123@cluster0.bunlk55.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()

#----------------SETTINGS------------------------
# Setting app config
st.set_page_config(page_title='Fields Info',
                   page_icon=':bar_chart:',
                   layout='wide'
                    )

#------------------------------------------------
st.write('''
# Lupatech  

Well Testing!
''')

@st.experimental_memo(ttl=600)
def get_data():
    db = client.example_db
    items = db.data1.find()
    items = list(items)  # make hashable for st.experimental_memo
    return items

items = get_data()

# Print results.
for item in items:
    st.write(f"{item['volumen']} has a :{item['masa']}:")

 

