from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import datetime

class WhatsAppHelper:
    
    current_time = datetime.datetime.now().time()
    
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
        #connect to db & retrive the first row from table
        db_file = "app_data.db"
        db_connect = sqlite3.connect(db_file)
        
        cursor = db_connect.cursor()
        cursor.execute("SELECT * FROM whatsapp_table")
        db_data = cursor.fetchall()
           
        for row in db_data:
            #return first row
            return row
        db_connect.close()
    
    def verify_execution_time(self,start_hour,end_hour):
        #checks if time is between  7 & 10 pm
        if self.current_time.hour >= start_hour and  self.current_time.hour <=end_hour:
            return True
        else:
            return False

    def click_whatsapp_logo(self):
        #click button after checking time condition else inform user about restriction
        if self.verify_execution_time(19,22):
            whatsapp_element = WebDriverWait(self.driver_obj,10).until(
                EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "WhatsApp"))
            )
            whatsapp_element.click()
        else:
            print("Goodnight message will only be sent out between the hours of 7 PM & 10PM. The current time is: " + str(self.current_time))

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
        try:
            send_button = WebDriverWait(self.driver_obj,10).until(
                EC.visibility_of_element_located((MobileBy.ACCESSIBILITY_ID, "Send")))
            send_button.click()
        except Exception as e:
            print("Unable to send message as the moment")
        finally:
           self.driver_obj.quit() 
    
