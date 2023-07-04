from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    chrome_option = Options()
    chrome_option.add_argument('lang=en_US')
    No_Image_loading = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", No_Image_loading)
    driver = webdriver.Chrome(options=chrome_option)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def search_view_by_name(driver):
    driver.get('https://www.youtube.com/results?search_query={}'.format('七里香 周杰伦'))
    


