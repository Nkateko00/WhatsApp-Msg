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
            whatsapp_element.click()

    def search_for_name(self,name):
        test_data = self.db_connection()
        search_input = WebDriverWait(self.driver_obj,10).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search"))
        )
        search_input.click()
        search_input.send_keys(test_data[1])  
        search_input.submit()
        
    def click_search_result(self):
        test_data = self.db_connection()
        name = test_data[1]
        contact_element = WebDriverWait(self.driver_obj,10).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, name))
        )
        contact_element.click()

    def send_msg(self,message):
        test_data = self.db_connection()
        msg_input = WebDriverWait(self.driver_obj,10).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID,"Write a message..."))
        )
        msg_input.send_keys(test_data[2])
  
    def click_send_msg(self):
        send_button = WebDriverWait(self.driver_obj,10).until(
            EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "Send")))
        send_button.click()

    def close_app(self):
        self.driver_obj.quit()
