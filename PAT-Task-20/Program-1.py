"""
PAT-Task-20 - Program-1
"""

# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Define a class Cowin to interact with the Cowin website
class Cowin:

    # Define XPATH locators for FAQ and Partners links
    FAQ_locator = '//*[@id="navbar"]/div[4]/div/div[1]/div/nav/div[3]/div/ul/li[4]/a'
    Partners_locator = '//*[@id="navbar"]/div[4]/div/div[1]/div/nav/div[3]/div/ul/li[5]/a'

    # Initialize the Cowin object with a URL
    def __init__(self,url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Login to the Cowin website
    def login(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.homepage_window_handle = self.driver.current_window_handle
        sleep(2)

    # Get the frame ID of FAQ and Partners pages
    def frame_id(self):
        # Click on the FAQ link
        self.driver.find_element(by=By.XPATH, value=self.FAQ_locator).click()
        # Get all window handles
        all_window_handle = self.driver.window_handles
        # Switch to the new window
        self.driver.switch_to.window(all_window_handle[1])
        # Print the frame ID of the FAQ page
        print("FAQ Frame ID is ," + self.driver.current_window_handle)
        sleep(2)
        # Close the FAQ window
        self.driver.close()
        # Switch back to the homepage window
        self.driver.switch_to.window(self.homepage_window_handle)

        # Click on the Partners link
        self.driver.find_element(by=By.XPATH, value=self.Partners_locator).click()
        # Get all window handles
        all_window_handle = self.driver.window_handles
        # Switch to the new window
        self.driver.switch_to.window(all_window_handle[1])
        # Print the frame ID of the Partners page
        print("Partner Frame ID is ," + self.driver.current_window_handle)
        sleep(2)
        # Close the Partners window
        self.driver.close()
        # Switch back to the homepage window
        self.driver.switch_to.window(self.homepage_window_handle)

    # Shutdown the browser
    def shutdown(self):
        # Quit the browser
        self.driver.quit()

# Create an instance of the Cowin class and call its methods
if __name__ == "__main__":
    url = "https://www.cowin.gov.in/"
    obj_cowin = Cowin(url)
    obj_cowin.login()
    obj_cowin.frame_id()
    obj_cowin.shutdown()