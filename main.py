import streamlit as st
import psycopg2
import pandas as pd

# Set up database connection
@st.cache_resource
def connect_db():
    return psycopg2.connect(
        dsn=st.secrets["db_url"]
    )

# Connect to DB
conn = connect_db()

# Title of the admin panel
st.title("Admin Panel - SaaS Dashboard")

# Fetch total number of users
def get_total_users():
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM user")
        total_users = cur.fetchone()[0]
    return total_users

# Fetch user table
def get_user_table():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM model")
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(data, columns=columns)

def get_all_tables():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
    return [table[0] for table in tables]


# Display total users
st.metric(label="Total Users", value=get_total_users())

# Display user table
st.write("### User Table")
st.dataframe(get_user_table())

# Fetch and display all tables
st.write("### Tables in the Database")
tables = get_all_tables()
st.write(tables)

# Close the connection when done
conn.close()
