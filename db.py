#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:34:37 2022

@author: oscarmejias
"""
#%%
from datetime import datetime
#%%
from pymongo import MongoClient

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://oscarmejias:oscar123@cluster0.bunlk55.mongodb.net/?retryWrites=true&w=majority"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)

db = client.get_database('example_db')
data = db.data2

print(data.count_documents({}))

# %%

new_record = {
    'date': datetime(2022,12,15,1),
    'masa': 48,
    'volumen': 1.17,
}

# %%
#data.insert_one(new_record)
# %%
import streamlit as st

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

st.dataframe(db.data.find())

# %%
