# 書目資料查詢入口
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from utils.utils import AlertHelper
from utils.utils import DropdownHelper

class UserInputHandler:
    '''UserInputHandlder for HomePage'''
    def __init__(self, page):
        self.input_type = None
        self.page = page
    
    def input_by_type(self):
        self.input_type = input("Enter your input type (Title, PublisherShortTitle, Date_Sales): ")
        self.page.switch_dropdown(self.input_type)
        return self.handle_input()
        
    
    def handle_input(self):

        if self.input_type == "Title":
            value = self.handle_title_input()
        elif self.input_type in ["PublisherShortTitle", "Date_Sales"]:
            value = self.handle_string_input()
        else:
            print("Invalid input type. Please enter a valid type.")
            raise TypeError
        
        self.page.search_value(value)
        return value
    
    def handle_title_input(self):
        while True:
            choice = input("Do you want to upload a file or enter a string? (file/string): ")
            if choice == "file":
                raise NotImplementedError
                # file_path = input("Enter the path to your file: ")
                # try:
                #     with open(file_path, 'r') as file:
                #         content = file.read()
                #         print("File content:")
                #         print(content)
                # except Exception as e:
                #     print(f"An error occurred: {e}")

            elif choice == "string":
                user_string = input("Enter your string: ")
                print("You entered:", user_string)
                return user_string
            else:
                print("Invalid choice. Please enter 'file' or 'string'.")
        
    def handle_string_input(self):
        user_string = input("Enter your string: ")
        print("You entered:", user_string)
        return user_string


class HomePage(object):
    
    # 查詢類型 / dropdown component
    category = (By.NAME, "FO_SearchField0")
    search_bar = (By.ID, "searchbook")
    btn = (By.CSS_SELECTOR, "button.btn.btn-blue.col-xs-12")

            
    def __init__(self, driver):
        self.driver = driver
    
    def _dropdowns(self):
        field = self.driver.find_element(*HomePage.category)
        return field
    
    def _dropdowns_values(self):
        field = self._dropdowns()
        options = field.find_elements(By.TAG_NAME, "option")
        res = []
        for option in options:
            res.append((option.get_attribute("value"), option.text))
        return res
    
    def _searchbar(self):
        field = self.driver.find_element(*HomePage.search_bar)
        return field
    
    def _submit_btn(self):
        field = self.driver.find_element(*HomePage.btn)
        return field


    def switch_dropdown(self, value):
        DropdownHelper().switch_dropdown(self._dropdowns, value)
        

    def search_value(self, value):
        search_bar = self._searchbar()
        search_bar.send_keys(value)
        submit_btn = self._submit_btn()
        submit_btn.click()
        alert_heler = AlertHelper(self.driver)
        alert = alert_heler.alert_is_present()
        if alert:
            print(value, "not found")
            alert_heler.accept_alert(alert)
            return 0
        else:
            return 1
            ...


