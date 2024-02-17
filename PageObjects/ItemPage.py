
from selenium.webdriver.common.by import By
from utils.utils import AlertHelper
class ItemPage(object):
    
    publish_info_table = (By.CSS_SELECTOR, 'table.table.table-bookinforight')
    next_page_btn = (By.CSS_SELECTOR, "a[aria-label='按鈕：下一頁']")

    isbn_info_table = (By.CSS_SELECTOR, 'table.rwd-table.table-bookinfo')
    isbn_field = (By.CSS_SELECTOR, "td[aria-label='ISBN(裝訂方式)']")
    date_field = (By.CSS_SELECTOR, "td[aria-label='出版年月']")
    def __init__(self, driver):
        self.driver = driver

        
    def next_page(self):
        field = self.driver.find_element(*ItemPage.next_page_btn)
        href = field.get_attribute('href')
        alert = AlertHelper(self.driver)
        if href :
            
            if alert.wait_till_clickable(ItemPage.next_page_btn):
                field.click()
                return True
            else:
                print("Unexpected Next Page Stop")
                return False
            
        else:
            return False
        
        
    def get_isbn_rows(self):
        table = self.driver.find_element(*ItemPage.isnb_info_table)
        rows = table.find_elements(By.TAG_NAME, "tr")
        return table

    def get_publisher_rows(self):
        table = self.driver.find_element(*ItemPage.publish_info_table)
        rows = table.find_elements(By.TAG_NAME, "tr")

        return rows
    


    @staticmethod
    def _get_col_val(row):
        return row.find_elements(By.TAG_NAME, "td")[1].text
       

    def _is_categorized(self, row):
        value = self._get_col_val(row).strip()
        
        if value == "&nbsp;&nbsp" or value == "  ":
            return None
        else:
            return value
        
    def _not_in_reading_range(self, row, reading_range = ["成人(一般)"]):
        value = self._get_col_val(row).strip()

        if value in reading_range:
            return False
        else:
            print(value, "not in reading range")
            return True
    
    def _is_restricted(self, row):
        value = self._get_col_val(row)
        if "限制級" in value:
            return True
        else:
            return False
        
        
        
    def scrape_book_info(self):

        publisher_rows = self.get_publisher_rows()

        if self._is_restricted(publisher_rows[9]):
            
            return {}
        if  self._not_in_reading_range(publisher_rows[8]):
            return {}
        
        category = self._is_categorized(publisher_rows[4]) # 圖書編號
        
        if not category:
            return {}
        

        title = self._get_col_val(publisher_rows[0])        # 書名
        author = self._get_col_val(publisher_rows[1])       # 作者
        publisher = self._get_col_val(publisher_rows[2])    # 出版商
        theme = self._get_col_val(publisher_rows[5])        # 主題標題
        isbn = self.driver.find_element(*ItemPage.isbn_field).text  # ISBN
        date = self.driver.find_element(*ItemPage.date_field).text  # 出版年月
        
                    
        return dict(title=title, author=author, publisher=publisher,
                    theme=theme, isbn=isbn, date=date)

        
    