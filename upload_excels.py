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
data = pd.read_excel('./data/data_example.xlsx')

# %%
data.head()

# %%
# Creates session and define context
session = Session.builder.configs(connection_parameters).create()
# If default is not set
session.use_database(config['default_database'])
session.use_schema(config['default_schema'])
session.use_warehouse(config['default_warehouse'])

# %%
session.write_pandas(data,"EXCEL_DATA_TABLE",auto_create_table=True)

# %%
session.close()