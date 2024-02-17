
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ISBNDriver(object):
    
    def __init__(self):
        service_obj = Service("/Users/joyjen/Desktop/100daysOfCode/selenium/chromedriver")
        self.driver = webdriver.Chrome(service=service_obj)
    
    def setup(self):
        HomePageUrl = "https://isbn.ncl.edu.tw/NEW_ISBNNet/"
        self.driver.get(HomePageUrl)
    
    def close(self):
        self.driver.close()