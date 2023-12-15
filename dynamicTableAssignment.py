import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class DynamicTableAssignment:
    # Initializing the variables
    def __init__(self, url):
        self.url = url  # Store the URL provided during class instantiation
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Set up the Chrome webdriver
        self.data_to_insert = None # Initialize data_to_insert attribute to None

    # Method to navigate to the page
    def navigate_to_page(self):
        self.driver.get(self.url) # Open the URL in the Chrome browser
        
    # In this method, inserting the data into the table 
    def insert_data_into_table(self, data):
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/details/summary').click() # Click on the details summary
        textarea = self.driver.find_element(By.ID, 'jsondata') # Locate the textarea element
        textarea.clear() # Clear any existing text in the textarea
        textarea.send_keys(data) # Enter the provided data into the textarea
        
        # Refreshing the table using the provided button
        refresh_button = self.driver.find_element(By.ID, 'refreshtable') # Locate the refresh button
        refresh_button.click() # Click the refresh button to update the table

    # In this method, asserting the data
    def assert_data_in_table(self, expected_data):
        try:
            table = self.driver.find_element(By.ID, 'dynamictable') # Locate the dynamic table
            rows = table.find_elements(By.TAG_NAME, 'tr') # Find all rows in the table

            for row_index, row in enumerate(rows):
                cells = row.find_elements(By.TAG_NAME, 'td')  # Find all cells in each row

                for cell_index, cell in enumerate(cells):
                    actual_data = cell.text.strip() # Get the text content of the cell

                    # Map cell_index to the corresponding key in the expected data
                    expected_data_key = "name" if cell_index == 0 else "age" if cell_index == 1 else "gender"

                    expected_data_cell = expected_data[row_index][expected_data_key] # Get the expected data value

                assert actual_data == str(expected_data_cell), f"Assertion failed for cell ({row_index + 1}, {cell_index + 1}): Expected '  {expected_data_cell}', Actual '{actual_data}'"

            return True  # All data matched successfully
        except Exception as e:
            return False  # Data is not yet present or does not match expected

    def close_browser(self):
        self.driver.quit() # Close the Chrome browser instance

if __name__ == "__main__":
    # Url to navigate
    url = 'https://testpages.herokuapp.com/styled/tag/dynamic-table.html'
    
    # Data to insert into the table    
    data_to_insert = '[{"name" : "Bob", "age" : 20, "gender": "male"}, {"name": "George", "age" : 42, "gender": "male"}, {"name": "Sara", "age" : 42, "gender": "female"}, {"name": "Conor", "age" : 40, "gender": "male"}, {"name": "Jennifer", "age" : 42, "gender": "female"}]'

    # Expected data for the assertion
    expected_data_for_assertion = [{"name" : "Bob", "age" : 20, "gender": "male"}, {"name": "George", "age" : 42, "gender": "male"}, {"name": "Sara", "age" : 42, "gender": "female"}, {"name": "Conor", "age" : 40, "gender": "male"}, {"name": "Jennifer", "age" : 42, "gender": "female"}]
    
    # Accessing the class
    automation = DynamicTableAssignment(url)

    try:
        # Navigate to the page using url
        automation.navigate_to_page()
        
        # In this method, inserting the data into the table 
        automation.insert_data_into_table(data_to_insert)
        
        # In this method, asserting the data
        automation.assert_data_in_table(expected_data_for_assertion)

        print("All data matched successfully!")
        
        time.sleep(10) # Introduce a sleep for 10 seconds for manual inspection


    finally:
        automation.close_browser() # Close the Chrome browser instance