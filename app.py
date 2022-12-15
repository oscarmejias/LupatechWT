#import pandas as pd
from pymongo import MongoClient
import streamlit as st

#---------------MONGODB CONNECTION---------------
@st.experimental_singleton
def init_connection():
    return MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_pswd@st.secrets.cluster_name.bunlk55.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()

#----------------SETTINGS------------------------
# Setting app config
#st.set_page_config(page_title='Fields Info',
#                   page_icon=':bar_chart:',
#                   layout='wide'
#                    )
#------------------------------------------------
st.write('''
# Lupatech  

Well Testing!
''')

@st.experimental_memo(ttl=600)
def get_data():
    db = client.get_database('example_db')
    data = list(db.data1.find()) # make hashable for st.experimental_memo
    return data

data = get_data()

# Print results.
for item in data:
    st.write(f"{data['volumen']} has a :{data['masa']}:")

 

