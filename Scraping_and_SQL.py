import time
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Create a WebDriverWait object
wait = WebDriverWait(driver, 20)

# Create an ActionChains object
actions = ActionChains(driver)

# List of RedBus links for different state transport corporations
links = [
    "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/west-bengal-transport-corporation?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/bihar-state-road-transport-corporation-bsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/pepsu/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/astc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile",
]

# Maximum number of pages to scrape for each transport corporation
max_pages = [5,3,2,5,1,4,4,3,5,4]

# Global lists to store route and bus details
all_route_details = []
final_details = []


def routes_and_links():
    """
    Finds all route links on the page and extracts their names and URLs,
    storing them in the all_route_details list.
    """
    try:
        # Find all route link elements
        routes_container = wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "route_link")
            )
        )
        for route in routes_container:
            try:
                # Extract route name and link
                route_name = route.find_element(By.CLASS_NAME, "route").text
                route_link = route.find_element(By.TAG_NAME, "a").get_attribute("href")
                all_route_details.append({
                    "route_name": route_name,
                    "route_link": route_link
                })
                        
            except Exception as e:
                print(f"routes and links Error: {e}")

    except Exception as e:
        print(f"routes and links Error: {e}")

def next_page_operator(current_page):
    """
    Navigate to the next page in the pagination.
    """
    try:
        # Locate the pagination container
        pagination_container = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')
            )
        )
        
        # Find and click the next page button
        next_page_button = pagination_container.find_element(
            By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{current_page + 1}"]'
        )
        actions.move_to_element(next_page_button).perform()
        driver.implicitly_wait(2)
        next_page_button.click()

        # Wait for the next page to load
        wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'),
                str(current_page + 1)
            )
        )
        driver.implicitly_wait(2)
    except Exception:
        print(f"next page operator Error: {e}")

def view_buses():
    """
    Finds and clicks all 'View Buses' buttons on the page.
    """
    try:
        # Find all 'View Buses' buttons
        b = driver.find_elements(By.CSS_SELECTOR,"div[class='button']")
        
        # Click buttons from bottom to top
        for i in range(len(b)-1,-1,-1):
            b[i].click()
            time.sleep(3)
    except Exception as e:
        print(f"view buses Error: {e}") 
        
def scroll_to_end():
    """
    Scroll to the bottom of the page to load all content.
    """
    try:
        # Initial page height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            # Check if page height has changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
    except Exception as e:
        print(f"scroll to end Error: {e}")

def elements(link, name):
    """
    Extract detailed bus information from the current page.
    """
    try:
        # Find elements for various bus details
        all_bus_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'travels lh-24 f-bold d-color')]")
        all_bus_types = driver.find_elements(By.XPATH, "//div[contains(@class, 'bus-type f-12 m-top-16 l-color evBus')]")
        all_departing_times = driver.find_elements(By.XPATH, "//div[contains(@class, 'dp-time f-19 d-color f-bold')]")
        all_durations = driver.find_elements(By.XPATH, "//div[contains(@class, 'dur l-color lh-24')]")
        all_reaching_times = driver.find_elements(By.XPATH, "//div[contains(@class, 'bp-time f-19 d-color disp-Inline')]")
        all_star_ratings = driver.find_elements(By.XPATH, "//div[@class='rating-sec lh-24']")
        all_prices = driver.find_elements(By.XPATH, "//div[contains(@class, 'fare d-block')]")
        all_seat_availabilities = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

        # Iterate through bus details and store in final_details
        for i in range(len(all_bus_names)):
            try:
                bus_elements = {
                    "route_name": name,
                    "route_link": link,
                    "busname": all_bus_names[i].text,
                    "bustype": all_bus_types[i].text,
                    "departing_time": all_departing_times[i].text,
                    "duration": all_durations[i].text,
                    "reaching_time": all_reaching_times[i].text,
                    "star_rating": all_star_ratings[i].text,
                    "price": all_prices[i].text,
                    "seats_available": all_seat_availabilities[i].text
                }
                final_details.append(bus_elements)

            except Exception as e:
                print(f"final_details Error: {e}")

    except Exception as e:
        print(f"elements Error: {e}")

def data_cleaning(df):
    """    
    Performs data type conversions and cleaning:
    - Removes 'INR' from price
    - Converts price to float
    - Cleans seat availability text
    - Converts seat availability to integer
    - Converts star rating to float
    """
    try:
        df['price'] = df['price'].str.replace('INR', '').astype(float)
        df['seats_available'] = df['seats_available'].str.replace(' Seats available', '')
        df['seats_available'] = df['seats_available'].str.replace(' Seat available', '')
        df['seats_available'] = df['seats_available'].astype(int)
        df['seats_available'] = df['seats_available'].fillna(0)
        df['star_rating'] = df['star_rating'].astype(float)
        df['star_rating'] = df['star_rating'].fillna(0)
        return df
    except Exception as e:
        print(f"data_cleaning Error: {e}")

def inserting_mysql(details):
    """
    Creates a 'bus_routes' table if it doesn't exist and 
    inserts all scraped bus details into the database.
    """
    try:
        # Establish MySQL connection
        mydb = mysql.connector.connect( 
        host="localhost",  
        user="root",      
        password="",
        database='bus_data',       
        )
        mycursor = mydb.cursor(buffered=True)

        # Create table if not exists
        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_routes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            route_name TEXT NOT NULL,
            route_link TEXT NOT NULL,
            busname TEXT NOT NULL, 
            bustype TEXT NOT NULL,
            departing_time TIME,
            duration TEXT NOT NULL,
            reaching_time TIME,
            star_rating FLOAT,
            price DECIMAL(10,2) NOT NULL,
            seats_available INT
        )
        """)

        # Insert each bus route detail
        for i in details:
            mycursor.execute("""
            INSERT INTO bus_routes (
                route_name, route_link,
                busname, bustype,
                departing_time, duration, reaching_time,
                star_rating, price,
                seats_available
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                i['route_name'], i['route_link'],
                i['busname'], i['bustype'],
                i['departing_time'], i['duration'], i['reaching_time'],
                i['star_rating'], i['price'], 
                i['seats_available']
            )
            )
        mydb.commit()

    except mysql.connector.Error as e:
        print(f"inserting_mysql Error: {e}")      

def all_bus_details(link,name):
    """
    Navigates to the route, expands bus details, 
    scrolls to load all content, and extracts bus information.
    """
    try:
        # Navigate to route link
        driver.get(link)
        driver.maximize_window()
        time.sleep(10)

        # Expand bus details
        view_buses()
        time.sleep(5)

        # Scroll to load all content
        scroll_to_end()
        time.sleep(3)

        # Extract bus elements
        elements(link,name)
    except Exception as e:
        print(f"all_bus_details Error:{e}")

def redbus_scraper():
    """
    Main scraping function to collect bus routes and details.
    
    Iterates through different state transport corporation links,
    scrapes route details, and then scrapes detailed bus information
    for each route. Saves route details to a CSV file.
    """

    # Scrape routes for each transport corporation
    for i in range(len(links)):
        driver.get(links[i])
        driver.maximize_window()
        driver.implicitly_wait(2)
        for current_page in range(1, max_pages[i]):
            routes_and_links()
            driver.implicitly_wait(2)
            next_page_operator(current_page)

    # Save route details to CSV        
    df = pd.DataFrame(all_route_details)
    df.to_csv("all_route_details.csv", index=False)

    # Scrape bus details for each route
    for i in all_route_details:
        link = i['route_link']
        name = i['route_name']
        all_bus_details(link,name)
    
if __name__ == "__main__":
    # Run the main scraping process
    redbus_scraper()

    # Clean and process collected bus details
    df2 = pd.DataFrame(final_details)
    df2 = data_cleaning(df2)
    final_details = df2.to_dict('records')

    # Insert details into MySQL database
    inserting_mysql(final_details)

    # Save bus details to CSV
    df2.to_csv("bus_routes.csv", index=False)
    print("Success")
