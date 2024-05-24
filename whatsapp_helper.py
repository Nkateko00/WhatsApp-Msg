from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3


# Set up Appium capabilities
class WhatsAppHelper:
    
    def __init__(self) :  
        desired_caps = {
            "platformName": "iOS",
            "platformVersion": "14.5",
            "deviceName": "iPhone 12",
            "automationName": "XCUITest",
            "app": "/path/to/WhatsApp.app"
        }
        self.driver_obj =  webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        
    def db_connection(self):
        db_file = "app_data.db"
        db_connect = sqlite3.connect(db_file)
        
        cursor = db_connect.cursor()
        cursor.execute("SELECT * FROM whatsapp_table")
        db_data =cursor.fetchall()
        
        for row in db_data:
            #return first row
            return row
        db_connect.close()


    def click_whatsapp_logo(self):
            whatsapp_element = WebDriverWait(self.driver_obj,10).until(
                EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "WhatsApp"))
            )
            # whatsapp_element = wait.until(EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "WhatsApp")))
            whatsapp_element.click()

    # Wait for the search input field to be visible
    def search_for_name(self,name):
        test_data = self.db_connection()
        search_input = WebDriverWait(self.driver_obj,10).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search"))
        )
        search_input.click()
        search_input.send_keys(test_data[1])  

    # search_input = wait.until(EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search")))
    # search_input.click()

    # # Enter the phone number
    # phone_number = "1234567890"
    # search_input.send_keys(phone_number)

    # Wait for the contact to be displayed and click on it
    # def
    # contact_element = wait.until(EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, phone_number)))
    # contact_element.click()

    # # Send a message
    # message_input = driver.find_element(MobileBy.ACCESSIBILITY_ID, "Write a message...")
    # message_input.send_keys("Hello, this is an automated message from Appium!")

    # Click the send button
    def send_msg(self):
        send_button = WebDriverWait(self.driver_obj,10).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "Send")))
        # send_button = driver.find_element(MobileBy.ACCESSIBILITY_ID, "Send")
        send_button.click()

    # Quit the Appium driver
    def close_app(self):
        self.driver_obj.quit()
