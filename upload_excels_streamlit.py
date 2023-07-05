# %%
import streamlit as st
import pandas as pd
import json
from snowflake.snowpark import Session

# %%
# Reads connection parameters from json config file
with open('./config.json','r') as file:
    config = json.load(file)

connection_parameters = {
    "account": config['account'],
    "user": config['user'],
    "password": config['password']
}

# %%
# Load data
with st.form("upload_file"): 
    uploaded_file = st.file_uploader("Select Excel file")
    uploaded = st.form_submit_button("Upload")
    if uploaded:
        df = pd.read_excel(uploaded_file)

# %%
# Creates session and define context
session = Session.builder.configs(connection_parameters).create()
# If default is not set
session.use_database(config['default_database'])
session.use_schema(config['default_schema'])
session.use_warehouse(config['default_warehouse'])

# %%
session.write_pandas(df,"EXCEL_DATA_TABLE",auto_create_table=True)

# %%
# Close sessions
session.close()