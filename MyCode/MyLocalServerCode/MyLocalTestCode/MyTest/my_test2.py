from selenium import webdriver

url = "https://music.youtube.com/browse/MPADUCO4AjeljgqgiowEf2yfvYHg"
driver = webdriver.Chrome()

driver.get(url)

print(driver.current_url)