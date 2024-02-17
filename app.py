
import os
import csv
from time import sleep

from main.conf import ISBNDriver
from PageObjects.HomePage import HomePage, UserInputHandler
from PageObjects.ListPage import ListPage, TableCrawler

if __name__ == "__main__":
    
    browser = ISBNDriver()
    browser.setup()

    home_page = HomePage(browser.driver)
    
    # This is static input from homepage
    input = UserInputHandler(home_page)
    input_value = input.input_by_type()
    
    page = ListPage(browser.driver)
    ctn = page.get_result_count()
    
    table = page.get_result_table()
    filename = os.path.join("output", f"{input_value}.csv")
    print(filename)
    crawler = TableCrawler(table=table, 
                           driver=browser.driver,
                           filename=filename)
    
    crawler.scrap()
    
    browser.close()

