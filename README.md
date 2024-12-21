# GUVI-DS-RedBus-Project
# Overview:
Web-Scraping bus data from RedBus website using Selenium.
Storing it in MySQL (XAMPP Server - Local Host).
Creating a Streamlit web application to view the bus details with filters and sortings.

# Scraping_and_SQL.py script overview:
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

####The data is also saved as a bus_routes.csv file for backup.
