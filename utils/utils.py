from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select

import csv
import os

class AlertHelper(object):
    def __init__(self, driver):
        self.driver = driver
    
    def alert_is_present(self, sec=3 ):
        wait = WebDriverWait(self.driver, sec)
        try:
            alert = wait.until(EC.alert_is_present())
            return alert
        except TimeoutException:
            return False
        
    def accept_alert(self, alert):
        alert.accept()
    
    def wait_till_clickable(self, path, sec=3):
        wait = WebDriverWait(self.driver, sec)
        try:
            wait.until(EC.element_to_be_clickable(path))
            return True
        except TimeoutException:
            return False
        
class DropdownHelper(object):
    
    def switch_dropdown(self, func,  value):
        field = Select(func())
        field.select_by_value(value)
    

class FileHelper(object):
    def append_to_csv(self, filename, fields):
        if len(fields) == 0:
            return
        with open(filename, 'a', encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(fields)