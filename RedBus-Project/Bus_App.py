import streamlit as st
import mysql.connector
import pandas as pd

# Create a database connection
mydb = mysql.connector.connect( 
host="localhost",  
user="root",      
password="",
database='bus_data',       
)
# Create a cursor object
mycursor = mydb.cursor(buffered=True)

# extracting from and to locations from route_name        
mycursor.execute("SELECT DISTINCT SUBSTRING_INDEX(route_name, ' ', 1) FROM bus_routes") # extracting from and to from route_name 
from_list = ['']
combination = []

# extracting from locations
for x in mycursor:
    from_list.append(x[0])

# extracting to locations
for i in from_list:
    to_list = ['']
    mycursor.execute(f"SELECT DISTINCT SUBSTRING_INDEX(route_name, ' to ', -1) FROM bus_routes WHERE route_name LIKE '{i}% to %'")
    for y in mycursor:
        to_list.append(y[0])
    combindict = {
        "from":i,
        "to":to_list
    }
    combination.append(combindict)

# setting layout as wide
st.set_page_config(layout="wide")

# title
st.title("Bus Details")

# sidebar
# Filters
st.sidebar.header("Filters")

# f - from, t - to, d - departure time
f = st.sidebar.selectbox("From",from_list)
t = st.sidebar.selectbox("To",combination[from_list.index(f)]["to"])
d = st.sidebar.radio("Departure Time",("Before 6 am","Between 6 am and 12 pm","Between 12 pm and 6 pm","After 6 pm"))

if d == "Before 6 am":
    t1 = "00:00:00"
    t2 = "06:00:00"
elif d == "Between 6 am and 12 pm":
    t1 = "06:00:00"
    t2 = "12:00:00"
elif d == "Between 12 pm and 6 pm":
    t1 = "12:00:00"
    t2 = "18:00:00"
else:
    t1 = "18:00:00"
    t2 = "24:00:00"

# p - price
p = st.sidebar.slider("Price Range", 0, 8000, (0, 8000))

p1 = float(p[0])
p2 = float(p[1])

# Sortings
st.sidebar.header("Sort")
sort = st.sidebar.radio("By",(
    "Departure Time","Arrival Time","Duration",
    "Price: low to high","Price: high to low",
    "Rating"))

if sort == "Departure Time":
    o = "departing_time"
elif sort == "Arrival Time":
    o = "reaching_time"
elif sort == "Duration":
    o = "duration"
elif sort == "Price: low to high":
    o = "price"
elif sort == "Price: high to low":
    o = "price DESC"
else:
    o = "star_rating DESC"

# SQL query to get bus details from database based on filters and sortings
mycursor.execute(f"""
    SELECT
        route_name,
        busname,bustype,
        DATE_FORMAT(departing_time, '%h:%i %p') as departing_time,
        duration,
        DATE_FORMAT(reaching_time, '%h:%i %p') as reaching_time,
        star_rating,price,seats_available,route_link,id
    FROM bus_routes
    WHERE route_name LIKE '{f}% to {t}%' AND
    departing_time BETWEEN '{t1}' AND '{t2}' AND
    price BETWEEN {p1} AND {p2}
    ORDER BY {o}

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





