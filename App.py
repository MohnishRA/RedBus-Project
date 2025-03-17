import mysql.connector
import streamlit as st
import pandas as pd

# Create a database connection
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "bus_data"
)
# Create a cursor object
mycursor = mydb.cursor(buffered=True)

# Extracting from locations     
mycursor.execute("SELECT DISTINCT SUBSTRING_INDEX(route_name, ' to ', 1) FROM bus_details")
from_list = ['']
for x in mycursor:
    from_list.append(x[0])

from_to_list = []
# extracting to locations
for i in from_list:
    to_list = ['']
    mycursor.execute(f"SELECT DISTINCT SUBSTRING_INDEX(route_name, ' to ', -1) FROM bus_details WHERE route_name LIKE '{i}%' ")
    for y in mycursor:
        to_list.append(y[0])
    # storing from and to locations
    from_to_dict = {
        "from":i,
        "to":to_list
    }
    from_to_list.append(from_to_dict)

# Setting page layout as wide
st.set_page_config(layout="wide")

# Title
st.title("Bus Details")

# Filters
st.sidebar.header("Filters")

# From and To Locations
from_location = st.sidebar.selectbox("From",from_list)
to_location = st.sidebar.selectbox("To",from_to_list[from_list.index(from_location)]["to"])

# Bus Type
mycursor.execute(f'SELECT DISTINCT bus_type FROM bus_details WHERE route_name = "{from_location} to {to_location}"')
bus_type_list = []
for x in mycursor:
    bus_type_list.append(x[0])
bus_type = st.sidebar.multiselect("Bus Type",bus_type_list)

# Departure Time
st.sidebar.write("Departure Time")
col1, col2 = st.sidebar.columns(2)
with col1:
    t1 = st.time_input("Between")
with col2:
    t2 = st.time_input("And")

# Price
price = st.sidebar.slider("Price Range", 0, 8000, (0, 8000))
start_price = float(price[0])
end_price = float(price[1])

# Rating
rating = st.sidebar.slider("Rating Range", 0.0, 5.0, (0.0, 5.0))
start_rating = float(rating[0])
end_rating = float(rating[1])

# Sortings
st.sidebar.header("Sort")
sort = st.sidebar.radio("By",(
    "Departure Time","Arrival Time","Duration",
    "Price: low to high","Price: high to low",
    "Rating"))

if sort == "Departure Time":
    order = "departing_time"
elif sort == "Arrival Time":
    order = "reaching_time"
elif sort == "Duration":
    order = "duration"
elif sort == "Price: low to high":
    order = "price"
elif sort == "Price: high to low":
    order = "price DESC"
else:
    order = "star_rating DESC"

if st.button("Show Bus Details"):
    # SQL query to get bus details from database based on filters and sortings
    mycursor.execute(f"""
        SELECT
            route_name,
            bus_name,bus_type,
            DATE_FORMAT(departing_time, '%h:%i %p') as departing_time,
            duration,
            DATE_FORMAT(reaching_time, '%h:%i %p') as reaching_time,
            star_rating,price,seats_available,route_link,id
        FROM bus_details
        WHERE route_name LIKE '{from_location} to {to_location}' AND
        bus_type IN ({",".join([f"'{x}'" for x in bus_type])}) AND
        departing_time BETWEEN '{t1}' AND '{t2}' AND
        price BETWEEN {start_price} AND {end_price} AND
        star_rating BETWEEN {start_rating} AND {end_rating}
        ORDER BY {order}
    """)

    # displaying bus details    
    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[
        "Route","Bus Name","Bus Type",
        "Departure Time","Duration","Arrival Time",
        "Rating","Price in Rs.","Seats Available",
        "Link","ID"])

    if len(df) == 0:
        # if no bus found 
        st.write("No bus found for the given filters and sortings.")
    else:
        # displaying bus details
        st.dataframe(df, width=4000, height=500)
