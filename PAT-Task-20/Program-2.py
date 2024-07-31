"""
PAT-Task-20 - Program-2
"""
import os.path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request

# Define a class Labour_Gov to automate tasks on the labour.gov.in website
class Labour_Gov:
    # Define XPATH locators for different elements on the website
    documents_locator = '//*[@id="nav"]/li[7]'
    monthly_progress_report_locator = '//*[@id="nav"]/li[7]/ul/li[2]/a'
    download_button_locator = '//*[@id="fontSize"]/div/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/a'
    media_locator = '//*[@id="nav"]/li[10]'
    photo_gallery_locator = '//*[@id="nav"]/li[10]/ul/li[2]/a'
    ILC_Session_112th_Locator = '112th Session of ILC'

    # Initialize the class with the website URL and folder paths for images and PDFs
    def __init__(self,url,images_folder_path,pdf_folder_path):
        self.url = url
        self.images_folder_path = images_folder_path
        self.pdf_folder_path = pdf_folder_path
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Start the automation by maximizing the window and navigating to the website
    def start_automation(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        # self.homepage_window_handle = self.driver.current_window_handle
        sleep(2)

    # Download the monthly progress report
    def download_monthly_progress(self):
        # Create an ActionChains object to perform mouse hover actions
        actions = ActionChains(self.driver)
        documents = self.driver.find_element(by=By.XPATH, value=self.documents_locator)
        actions.move_to_element(documents)
        actions.perform()
        # Click on the monthly progress report link
        self.driver.find_element(by=By.XPATH, value=self.monthly_progress_report_locator).click()
        # Click on the download button
        self.driver.find_element(by=By.XPATH, value=self.download_button_locator).click()
        # Accept the alert
        alert = self.driver.switch_to.alert
        alert.accept()
        # Switch to the new window
        all_window_handle = self.driver.window_handles
        self.driver.switch_to.window(all_window_handle[1])
        # Download the PDF file
        filename = "June-2024-Monthly-Report.pdf"
        filepath = os.path.join(self.pdf_folder_path, filename)
        urllib.request.urlretrieve(self.driver.current_url, filepath)
        print(f"Downloaded {filename}")
        sleep(3)
        # Check if the correct PDF file was downloaded
        if self.driver.current_url == "https://labour.gov.in/sites/default/files/mpr_for_june_2024.pdf":
            print("Successfully downloaded the monthly progress report for June 2024")
        # Switch back to the original window
        self.driver.switch_to.window(all_window_handle[0])
        sleep(2)

    # Download images from the photo gallery
    def download_images(self):
        # Create an ActionChains object to perform mouse hover actions
        actions = ActionChains(self.driver)
        # Find the media element and hover over it
        documents = self.driver.find_element(by=By.XPATH, value=self.media_locator)
        actions.move_to_element(documents)
        actions.perform()
        # Click on the photo gallery link
        self.driver.find_element(by=By.XPATH, value=self.photo_gallery_locator).click()
        # Click on the 112th Session of ILC link
        self.driver.find_element(by=By.LINK_TEXT, value=self.ILC_Session_112th_Locator).click()
        # Find all image elements on the page
        images = self.driver.find_elements(by=By.TAG_NAME,value='img')
        # Getting source of each image
        # for i in images:
        #     src = i.get_attribute('src')
        #     print(src)
        # Download each image
        for i in range(len(images)):
            src = images[i].get_attribute('src')
            if src:
                filename = f"image_{i+1}.jpg"
                filepath = os.path.join(self.images_folder_path, filename)
                urllib.request.urlretrieve(src,filepath)
                print(f"Downloaded {filename}")
        sleep(3)


# Main program
if __name__ == "__main__":
    url = "https://labour.gov.in/"
    images_folder_path = "images"  # create a folder named "images" in the same directory
    pdf_folder_path = "pdf"
    if not os.path.exists(images_folder_path):
        os.makedirs(images_folder_path)
    if not os.path.exists(pdf_folder_path):
        os.makedirs(pdf_folder_path)
    obj_labour_gov = Labour_Gov(url, images_folder_path,pdf_folder_path)
    obj_labour_gov.start_automation()
    obj_labour_gov.download_monthly_progress()
    obj_labour_gov.download_images()
