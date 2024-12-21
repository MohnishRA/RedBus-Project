# GUVI-DS-RedBus-Project

# Content:
    A) Overview
    B) Scraping_and_SQL.py Script Explanation
    C) Bus_App.py Script Explanation
    
# A) Overview:
Web-Scraping bus data from redbus website ([https://www.redbus.in/](url)) using selenium and storing it in MySQL (XAMPP server - localhost).
Creating a streamlit web application in a virtual environment to view the bus details with filters and sortings.


# B) Scraping_and_SQL.py Script Explanation:
This Python script is designed to scrape bus route and bus details from various state transport corporations websites through RedBus. The script uses Selenium WebDriver for web scraping, pandas for data manipulation, and MySQL for data storage.

## Python libraries:
  1. time: For adding delays during web scraping
  2. pandas: For data manipulation and CSV export
  3. mysql.connector: For MySQL database operations
 
## Selenium libraries:
  1. webdriver: For browser automation
  2. ActionChains: For complex browser interactions
  3. WebDriverWait: For handling dynamic page loading
  4. expected_conditions: For defining wait conditions
     
## Global Variables:
  1. links: A list of RedBus URLs for different state transport corporations
  2. max_pages: Maximum number of pages to scrape for each transport corporation
  3. all_route_details: Stores route information
  4. final_details: Stores detailed bus information
     
## Functions:
### redbus_scraper():
Main scraping function to collect bus routes and details
  1. Iterates through transport corporation links
  2. Scrapes route details
  3. Saves route details to CSV
  4. Scrapes detailed bus information for each route

### routes_and_links():
Extracts route names and URLs from the current page
  1. Finds elements with class route_link
  2. Extracts route name and URL
  3. Stores in all_route_details list
     
### next_page_operator(current_page):
Navigate to the next page in pagination
  1. Locates pagination container
  2. Finds and clicks the next page button
  3. Waits for the page to load
   
### all_bus_details(link, name):
Collect comprehensive bus details for a specific route
  1. Navigates to route link
  2. Maximizes browser window
  3. Expands bus details
  4. Scrolls to load all content
  5. Extracts bus elements
     
### view_buses():
Expand bus details on the page
  1. Finds all 'View Buses' buttons
  2. Clicks buttons from bottom to top
  3. Adds a small delay between clicks

### scroll_to_end():
Scroll to the bottom of the page to load all content
  1. Repeatedly scrolls to the bottom
  2. Checks if page height changes
  3. Stops when no more content is loaded

### elements(link, name):
Extract detailed bus information from the current page
  1. Finds elements for bus details:
        a. Bus names
        b. Bus types
        c. Departing times
        d. Durations
        e. Reaching times
        f. Star ratings
        g. Prices
        h. Seat availabilities
  2. Stores extracted information in final_details

### data_cleaning(df):
Clean and process scraped data
  1. Removes 'INR' from price
  2. Converts price to float
  3. Cleans seat availability text
  4. Converts seat availability to integer
  5. Converts star rating to float

### inserting_mysql(details):
Store scraped bus details in MySQL database
  1. Establishes MySQL connection
  2. Creates bus_routes table if not exists
  3. Inserts bus details into the table
  4. Database Schema:
        a. id: Auto-incrementing primary key
        b. route_name: Text
        c. route_link: Text
        d. busname: Text
        e. bustype: Text
        f. departing_time: Time
        g. duration: Text
        h. reaching_time: Time
        i. star_rating: Float
        j. price: Decimal
        k. seats_available: Integer

#### The data is also saved as a bus_routes.csv file for backup.


# C) Bus_App.py Script Explanation:
This script is created in a virtual environment to run a streamlit web application with MySQL database. The application allows users to search for bus details with various filters and sorting options.

## Libraries:
  1. streamlit: Web application framework
  2. mysql.connector: MySQL database connection library
  3. pandas: Data manipulation library

## Database Connection:
Establishes a connection to a XAMPP server - local MySQL database named 'bus_data'. Creates a cursor object for executing SQL queries.

## Route Location Extraction:
### From Locations:
  1. Extracts unique "From" locations from the route_name column.
  2. Populates from_list with distinct starting locations
     
### To Locations:
  1. For each "From" location, extracts corresponding "To" locations.
  2. Creates a list of dictionaries mapping "From" locations to their possible "To" destinations

## Streamlit Application Setup
### Page Configuration:
  1. Sets the page layout to wide
  2. Adds “Bus Details” as title to the application

### Location Selection Filter:
  1. Provides dropdown menus for selecting "From" and "To" locations
  2. Dynamically updates "To" locations based on selected "From" location

### Departure Time Filter:
  1. Allows filtering buses by time of day
  2. Converts selected time range to specific time boundaries

### Price Range Slider:
  1. Provides a slider to filter buses by price range
  2. Default range is 0 to 8000 Rs.

### Sorting Options:
  1. Departure Time
  2. Arrival Time
  3. Duration
  4. Price: low to high
  5. Price: high to low
  6. Rating

### SQL Query Generation:
  1. Generates a dynamic SQL query based on user-selected filters
  2. Applies filters for:
        a. Route name
        b. Departure time
        c. Price range
  3. Applies selected sorting criteria

### Display Results:
  1. Fetches query results
  2. Converts results to a pandas DataFrame
  3. If buses found it displays the results in a Streamlit dataframe.
  4. If buses not found it displays “No bus found for the given filters and sortings.”


## Screenshots of the streamlit web-application also uploaded.
