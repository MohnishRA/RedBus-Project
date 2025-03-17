import time
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

# Initializing Chrome WebDriver
driver = webdriver.Chrome()

# Creating WebDriverWait object
wait = WebDriverWait(driver, 20)

# Creating ActionChains object
actions = ActionChains(driver)


# Global lists to store route and bus details
route_details = []
bus_details = []


def routes_and_links():
    """
    Finds all route links on the page and extracts their names and URLs,
    storing them in the route_details list.
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
                route_details.append({
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
    except Exception as e:
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
        scrolling=True
        time.sleep(10)
        while scrolling:
            old_page_source = driver.page_source
            body=driver.find_element(By.XPATH,"/html/body")
            wait.until(EC.presence_of_all_elements_located((By.XPATH,"/html/body")))
            body.send_keys(Keys.END)
            time.sleep(3)
            new_page_source=driver.page_source
            if new_page_source == old_page_source:
                scrolling=False
        
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
                    "bus_name": all_bus_names[i].text,
                    "bus_type": all_bus_types[i].text,
                    "departing_time": all_departing_times[i].text,
                    "duration": all_durations[i].text,
                    "reaching_time": all_reaching_times[i].text,
                    "star_rating": all_star_ratings[i].text if i < len(all_star_ratings) else '0',
                    "price": all_prices[i].text,
                    "seats_available": all_seat_availabilities[i].text
                }
                bus_details.append(bus_elements)

            except Exception as e:
                print(f"final_details Error: {e}")

    except Exception as e:
        print(f"elements Error: {e}")

def redbus_scraper():
    """
    Main scraping function to collect routes and bus details.
    
    Iterates through different state transport corporation links,
    scrapes route details, and then scrapes detailed bus information
    for each route.
    """

    # List of RedBus links for different state transport corporations
    links = [
        "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/west-bengal-transport-corporation?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/bihar-state-road-transport-corporation-bsrtc/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/astc/?utm_source=rtchometile",
        "https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile",
    ]

    # Maximum number of pages in each state transport corporation
    max_pages = [5,4,2,5,1,5,4,4,4]

    # Scrape routes for each transport corporation
    for i in range(len(links)):
        driver.get(links[i])
        driver.maximize_window()
        driver.implicitly_wait(2)
        for current_page in range(1, max_pages[i]):
            routes_and_links()
            driver.implicitly_wait(2)
            next_page_operator(current_page)

    # Scrape bus details for each route
    for i in route_details:
        link = i['route_link']
        name = i['route_name']

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
    
if __name__ == "__main__":
    # Function to scrape bus details
    redbus_scraper()

    # Convert bus details to DataFrame
    df = pd.DataFrame(bus_details)

    # Save bus details as a CSV file
    df.to_csv("bus_rfoutes.csv", index=False)
    print("Success")
