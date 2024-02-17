
from selenium.webdriver.common.by import By
from utils.utils import DropdownHelper, FileHelper
from PageObjects.ItemPage import ItemPage


class ListPage(object):
    """ListPage is a result page after query"""
    
    # 查詢結果
    result_tbl = (By.ID, 'ResultBox')
    # 查詢結果之數量
    result_cnt = (By.CLASS_NAME, "text-right-ISBN")
   
    # 排序
    tbl_sort_field = (By.NAME, "FO_資料排序")
    # 每頁筆數
    tbl_page_field = (By.NAME, "FO_每頁筆數")
    
    # 篩選 - 適讀對象
    filter_age = (By.XPATH, "//a[contains(@href,'Aud=161')]") #成人(一般)

    def __init__(self, driver):
        self.driver = driver
        self.load_limit = "50"
    
    
    def get_result_table(self):
        table = self.driver.find_element(*ListPage.result_tbl)
        return table
    
    def get_result_count(self):
        table = self.get_result_table()
        ctn = table.find_element(*ListPage.result_cnt).text
        print(ctn)
        return ctn

    def _sort_table(self):
        return self.driver.find_element(*ListPage.tbl_sort_field)

    def _filter_table(self):
        return self.driver.find_element(*ListPage.tbl_page_field)
    
    def sort(self):
        DropdownHelper().switch_dropdown(
            self._sort_table,
            "PubMonth_Pre DESC")
    
    def pagination(self):
        DropdownHelper().switch_dropdown(
            self._filter_table,
            self.load_limit)
        
    # def filter(self):
    #     filter_field_1 = self.driver.find_element(*ListPage.filter_age)
    #     filter_field_1.click()
    #     print("apply filter")
            
class TableCrawler(object):
    
    first_row = (By.CSS_SELECTOR, "a[href='main_DisplayRecord.php?&Pact=init&Pstart=1']")
    
    def __init__(self, table, driver, filename):
        self.table = table
        self.driver = driver
        self.item_limit = 3000 
        self.filename = filename

        
    
    def scrap(self):

        # 選擇第一筆detail
        starter = self.table.find_element(*TableCrawler.first_row)
        starter.click()
        item_counter = 1

        # 抓取資料
        detail = ItemPage(self.driver)
        res = detail.scrape_book_info()
        file = FileHelper()


        file.append_to_csv(
            filename=self.filename,
            fields=list(res.values())
        )
        
        
        # 如果有下一頁且在page_limit範圍內:
        while detail.next_page():
            if item_counter > self.item_limit:
                # 避免 Abuse 資料庫
                break

            # 抓取資料
            res = detail.scrape_book_info()

            file.append_to_csv(
                filename=self.filename,
                fields=list(res.values())
            )

            item_counter +=1
            
            if item_counter % 100 == 0:
                print(f"You have been process {item_counter} items", end="\r")
            
            
