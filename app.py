import streamlit as st
import sqlite3
import pandas as pd

# Helper function to get DB connection
def get_connection():
    conn = sqlite3.connect('food_wastage.db', check_same_thread=False)
    return conn

conn = get_connection()
cursor = conn.cursor()
st.title("Local Food Wastage Management System")

query_options = {
    "1. Providers per city": """
        SELECT City, COUNT(DISTINCT Provider_ID) AS Num_Providers FROM Providers GROUP BY City;
    """,
    "2. Receivers per city": """
        SELECT City, COUNT(DISTINCT Receiver_ID) AS Num_Receivers FROM Receivers GROUP BY City;
    """,
    "3. Top provider types by contribution": """
        SELECT P.Type, COUNT(F.Food_ID) AS Food_Contribution
        FROM Providers P
        JOIN Food_Listings F ON P.Provider_ID = F.Provider_ID
        GROUP BY P.Type
        ORDER BY Food_Contribution DESC;
    """,
    # Add more predefined queries here...
}

selected_query = st.sidebar.selectbox("Select a SQL Query to Display", list(query_options.keys()))

if selected_query:
    df = pd.read_sql_query(query_options[selected_query], conn)
    st.subheader(selected_query)
    st.dataframe(df)
st.sidebar.subheader("Add New Food Listing")

with st.sidebar.form(key='add_food_form', clear_on_submit=True):
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    expiry_date = st.date_input("Expiry Date")
    provider_id = st.number_input("Provider ID", min_value=1, step=1)
    provider_type = st.text_input("Provider Type")
    location = st.text_input("Location (City)")
    food_type = st.selectbox("Food Type", ['Vegetarian', 'Non-Vegetarian', 'Vegan'])
    meal_type = st.selectbox("Meal Type", ['Breakfast', 'Lunch', 'Dinner', 'Snacks'])
    
    submitted = st.form_submit_button("Add Food Listing")
    if submitted:
        cursor.execute('''
            INSERT INTO Food_Listings
            (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (food_name, quantity, expiry_date.strftime("%Y-%m-%d"), provider_id, provider_type, location, food_type, meal_type))
        conn.commit()
        st.success(f"Food Listing '{food_name}' added successfully!")
st.sidebar.subheader("Update Food Quantity")

with st.sidebar.form(key='update_food_form'):
    food_id_update = st.number_input("Food ID to Update", min_value=1, step=1)
    new_quantity = st.number_input("New Quantity", min_value=1, step=1)
    
    update_submitted = st.form_submit_button("Update Quantity")
    if update_submitted:
        cursor.execute('''
            UPDATE Food_Listings
            SET Quantity = ?
            WHERE Food_ID = ?
        ''', (new_quantity, food_id_update))
        conn.commit()
        st.success(f"Updated quantity for Food_ID {food_id_update} to {new_quantity}.")
st.sidebar.subheader("Delete Food Listing")

with st.sidebar.form(key='delete_food_form'):
    food_id_delete = st.number_input("Food ID to Delete", min_value=1, step=1)
    delete_submitted = st.form_submit_button("Delete Food Listing")
    if delete_submitted:
        cursor.execute('DELETE FROM Food_Listings WHERE Food_ID = ?', (food_id_delete,))
        conn.commit()
        st.success(f"Deleted Food Listing with Food_ID {food_id_delete}.")
st.header("Filter Food Listings")

city_filter = st.selectbox("Filter by City", ['All'] + [row[0] for row in cursor.execute("SELECT DISTINCT Location FROM Food_Listings").fetchall()])
provider_type_filter = st.multiselect("Filter by Provider Type", [row for row in cursor.execute("SELECT DISTINCT Provider_Type FROM Food_Listings").fetchall()])
food_type_filter = st.multiselect("Filter by Food Type", ['Vegetarian', 'Non-Vegetarian', 'Vegan'])
meal_type_filter = st.multiselect("Filter by Meal Type", ['Breakfast', 'Lunch', 'Dinner', 'Snacks'])

query = "SELECT * FROM Food_Listings WHERE 1=1"

if city_filter != 'All':
    query += f" AND Location = '{city_filter}'"
if provider_type_filter:
    provider_types = "', '".join(provider_type_filter)
    query += f" AND Provider_Type IN ('{provider_types}')"
if food_type_filter:
    foods = "', '".join(food_type_filter)
    query += f" AND Food_Type IN ('{foods}')"
if meal_type_filter:
    meals = "', '".join(meal_type_filter)
    query += f" AND Meal_Type IN ('{meals}')"

df_filtered = pd.read_sql_query(query, conn)
st.dataframe(df_filtered)

# Show contact details of providers for filtered food listings
st.subheader("Provider Contacts for Filtered Food")

if not df_filtered.empty:
    provider_ids = df_filtered['Provider_ID'].unique().tolist()
    placeholders = ','.join(['?']*len(provider_ids))
    providers_query = f"SELECT Name, Contact, City FROM Providers WHERE Provider_ID IN ({placeholders})"
    providers_df = pd.read_sql_query(providers_query, conn, params=provider_ids)
    st.dataframe(providers_df)
else:
    st.write("No food listings found for the selected filters.")
