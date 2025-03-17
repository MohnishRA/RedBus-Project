# Bus Details Scraping

This project scrapes bus details, preprocesses the data, stores it in a database using SQL, and provides an interactive application for users to filter and view bus information.

## Features:
1. **Bus_Details_Scraping** - Scrapes bus route details and saves them as a CSV file.
2. **Data_Preprocessing** - Cleans and processes the scraped.
3. **SQL** - Stores the processed data in a MySQL database.
4. **App** - Provides a Streamlit-based UI to explore bus details interactively.

## Prerequisites
- Python
- MySQL Server
- Required Python libraries:
  ```sh
  pip install selenium pandas mysql-connector-python streamlit
  ```
**NOTE:** streamlit script 'app.py' should be run in a virtual environment. In the virtual environment install streamlit, mysql-connector-python, pandas and run the script.

## Usage
### Step 1: Run the Scraper
```sh
python Bus_Details_Scraping.py
```
This will generate a CSV file with bus route details.

### Step 2: Data Preprocessing
Open `Data_Preprocessing.ipynb` in Jupyter Notebook and run all cells to clean the data.
**NOTE:** You need to look at the bus type as it may change.

### Step 3: Load Data into MySQL
Run the SQL scripts in `SQL.ipynb` to create the necessary database and import the processed data.

### Step 4: Launch the Application
```sh
streamlit run app.py
```
This starts the interactive streamlit app where you can filter and sort buses in various ways.
